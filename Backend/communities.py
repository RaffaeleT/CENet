from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_db, require_role
import models
import schemas

router = APIRouter(prefix="/communities", tags=["Communities"])


@router.post("/", response_model=schemas.EnergyCommunityResponse, status_code=status.HTTP_201_CREATED)
def create_community(
    community: schemas.EnergyCommunityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    db_community = models.EnergyCommunity(
        name=community.name,
        province=community.province,
        region=community.region,
        description=community.description,
        manager_id=current_user.id,
        status="draft"
    )

    db.add(db_community)
    db.commit()
    db.refresh(db_community)

    return db_community


@router.get("/my", response_model=list[schemas.EnergyCommunityResponse])
def get_my_communities(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    return (
        db.query(models.EnergyCommunity)
        .filter(models.EnergyCommunity.manager_id == current_user.id)
        .all()
    )


@router.get("/{community_id}", response_model=schemas.EnergyCommunityResponse)
def get_community(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
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