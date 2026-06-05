import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_db, require_role
import models
import schemas

router = APIRouter(prefix="/simulations", tags=["Simulations"])


def calculate_roi_result(data: schemas.ROISimulationCreate) -> dict:
    yearly_savings = data.annual_kwh * data.electricity_price * 0.35
    yearly_incentive = data.annual_kwh * data.incentive_rate
    yearly_benefit = yearly_savings + yearly_incentive
    payback_years = data.installation_cost / yearly_benefit if yearly_benefit > 0 else None

    return {
        "yearly_savings": round(yearly_savings, 2),
        "yearly_incentive": round(yearly_incentive, 2),
        "yearly_benefit": round(yearly_benefit, 2),
        "payback_years": round(payback_years, 2) if payback_years else None,
    }


def calculate_sme_result(data: schemas.SMESimulationCreate) -> dict:
    battery_bonus = data.battery_size_kwh * 25
    yearly_savings = data.annual_kwh * data.electricity_price * 0.40 + battery_bonus
    yearly_incentive = data.annual_kwh * data.incentive_rate
    yearly_benefit = yearly_savings + yearly_incentive
    payback_years = data.installation_cost / yearly_benefit if yearly_benefit > 0 else None

    return {
        "yearly_savings": round(yearly_savings, 2),
        "yearly_incentive": round(yearly_incentive, 2),
        "yearly_benefit": round(yearly_benefit, 2),
        "payback_years": round(payback_years, 2) if payback_years else None,
        "battery_bonus": round(battery_bonus, 2),
        "company_size": data.company_size,
        "sector": data.sector,
    }


@router.post("/roi", response_model=schemas.SimulationResponse, status_code=status.HTTP_201_CREATED)
def create_roi_simulation(
    simulation: schemas.ROISimulationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["user", "operator", "supplier"]))
):
    result = calculate_roi_result(simulation)

    db_simulation = models.Simulation(
        user_id=current_user.id,
        simulation_type="roi",
        title=simulation.title,
        input_data=json.dumps(simulation.model_dump()),
        result_data=json.dumps(result)
    )

    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)

    return db_simulation


@router.post("/sme", response_model=schemas.SimulationResponse, status_code=status.HTTP_201_CREATED)
def create_sme_simulation(
    simulation: schemas.SMESimulationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["user", "operator", "supplier"]))
):
    result = calculate_sme_result(simulation)

    db_simulation = models.Simulation(
        user_id=current_user.id,
        simulation_type="sme",
        title=simulation.title,
        input_data=json.dumps(simulation.model_dump()),
        result_data=json.dumps(result)
    )

    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)

    return db_simulation


@router.get("/", response_model=list[schemas.SimulationResponse])
def get_my_simulations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["user", "operator", "supplier"]))
):
    return (
        db.query(models.Simulation)
        .filter(models.Simulation.user_id == current_user.id)
        .order_by(models.Simulation.created_at.desc())
        .all()
    )


@router.get("/{simulation_id}", response_model=schemas.SimulationResponse)
def get_simulation_by_id(
    simulation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["user", "operator", "supplier"]))
):
    simulation = (
        db.query(models.Simulation)
        .filter(
            models.Simulation.id == simulation_id,
            models.Simulation.user_id == current_user.id
        )
        .first()
    )

    if simulation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Simulation not found"
        )

    return simulation