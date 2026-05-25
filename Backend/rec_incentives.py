import csv
import io

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth import get_db, require_role
from event_logs import log_event
import models
import schemas

router = APIRouter(prefix="/rec-incentives", tags=["REC Incentives"])


def get_owned_community(db: Session, community_id: int, current_user: models.User):
    if current_user.role == "admin":
        community = (
            db.query(models.EnergyCommunity)
            .filter(models.EnergyCommunity.id == community_id)
            .first()
        )
    else:
        community = (
            db.query(models.EnergyCommunity)
            .filter(
                models.EnergyCommunity.id == community_id,
                models.EnergyCommunity.manager_id == current_user.id
            )
            .first()
        )

    if community is None:
        raise HTTPException(status_code=404, detail="Community not found")

    return community


@router.post("/{community_id}/prices", response_model=schemas.EnergyPriceResponse, status_code=status.HTTP_201_CREATED)
def create_energy_price(
    community_id: int,
    price: schemas.EnergyPriceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    db_price = models.EnergyPrice(
        community_id=community_id,
        price_eur_kwh=price.price_eur_kwh,
        valid_from=price.valid_from,
        valid_to=price.valid_to,
        created_by=current_user.id
    )

    db.add(db_price)
    db.commit()
    db.refresh(db_price)

    return db_price


@router.post("/{community_id}/costs", response_model=schemas.CommunityCostResponse, status_code=status.HTTP_201_CREATED)
def create_community_costs(
    community_id: int,
    costs: schemas.CommunityCostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    db_costs = models.CommunityCost(
        community_id=community_id,
        fixed_management_cost=costs.fixed_management_cost,
        variable_cost=costs.variable_cost,
        created_by=current_user.id
    )

    db.add(db_costs)
    db.commit()
    db.refresh(db_costs)

    return db_costs


@router.post("/gse-parameters", response_model=schemas.GSEIncentiveParameterResponse, status_code=status.HTTP_201_CREATED)
def create_gse_parameter(
    parameter: schemas.GSEIncentiveParameterCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    db_parameter = models.GSEIncentiveParameter(
        name=parameter.name,
        tariff_eur_kwh=parameter.tariff_eur_kwh,
        description=parameter.description,
        valid_from=parameter.valid_from,
        valid_to=parameter.valid_to
    )

    db.add(db_parameter)
    db.commit()
    db.refresh(db_parameter)

    return db_parameter


@router.post("/{community_id}/calculate", response_model=list[schemas.IncentiveAllocationResponse])
def calculate_incentive_allocation(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    latest_tariff = (
        db.query(models.GSEIncentiveParameter)
        .order_by(models.GSEIncentiveParameter.created_at.desc())
        .first()
    )

    tariff = latest_tariff.tariff_eur_kwh if latest_tariff else 0.11

    total_shared = (
        db.query(func.coalesce(func.sum(models.RECEnergyReading.kwh_shared), 0))
        .filter(models.RECEnergyReading.community_id == community_id)
        .scalar()
    )

    latest_costs = (
        db.query(models.CommunityCost)
        .filter(models.CommunityCost.community_id == community_id)
        .order_by(models.CommunityCost.created_at.desc())
        .first()
    )

    fixed_costs = latest_costs.fixed_management_cost if latest_costs else 0
    variable_costs = latest_costs.variable_cost if latest_costs else 0
    total_costs = fixed_costs + variable_costs

    gross_total_incentive = total_shared * tariff
    net_distributable = max(gross_total_incentive - total_costs, 0)

    member_rows = (
        db.query(
            models.CommunityMember.user_id,
            models.CommunityMember.pod_id,
            func.coalesce(func.sum(models.RECEnergyReading.kwh_shared), 0)
        )
        .outerjoin(
            models.RECEnergyReading,
            models.CommunityMember.pod_id == models.RECEnergyReading.pod_id
        )
        .filter(models.CommunityMember.community_id == community_id)
        .group_by(models.CommunityMember.user_id, models.CommunityMember.pod_id)
        .all()
    )

    db.query(models.IncentiveAllocation).filter(
        models.IncentiveAllocation.community_id == community_id
    ).delete(synchronize_session=False)

    allocations = []

    for user_id, pod_id, member_shared in member_rows:
        share_ratio = member_shared / total_shared if total_shared > 0 else 0
        gross_incentive = gross_total_incentive * share_ratio
        cost_share = total_costs * share_ratio
        net_reimbursement = net_distributable * share_ratio

        allocation = models.IncentiveAllocation(
            community_id=community_id,
            member_user_id=user_id,
            gross_incentive=round(gross_incentive, 2),
            cost_share=round(cost_share, 2),
            net_reimbursement=round(net_reimbursement, 2)
        )

        db.add(allocation)
        allocations.append(allocation)

    db.commit()

    for allocation in allocations:
        db.refresh(allocation)

    log_event(
        db=db,
        event_type="incentive_allocation_calculated",
        user_id=current_user.id,
        details={
            "community_id": community_id,
            "gross_total_incentive": round(gross_total_incentive, 2),
            "total_costs": round(total_costs, 2),
            "net_distributable": round(net_distributable, 2)
        }
    )

    return allocations


@router.get("/{community_id}/allocation", response_model=list[schemas.IncentiveAllocationResponse])
def get_incentive_allocation(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    return (
        db.query(models.IncentiveAllocation)
        .filter(models.IncentiveAllocation.community_id == community_id)
        .order_by(models.IncentiveAllocation.net_reimbursement.desc())
        .all()
    )


@router.get("/{community_id}/export")
def export_incentive_allocation_csv(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    allocations = (
        db.query(models.IncentiveAllocation)
        .filter(models.IncentiveAllocation.community_id == community_id)
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "member_user_id",
        "gross_incentive",
        "cost_share",
        "net_reimbursement",
        "created_at"
    ])

    for item in allocations:
        writer.writerow([
            item.member_user_id,
            item.gross_incentive,
            item.cost_share,
            item.net_reimbursement,
            item.created_at.isoformat() if item.created_at else ""
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=allocation_report_{community_id}.csv"
        }
    )