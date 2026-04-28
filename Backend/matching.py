from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth import get_db, require_role
import models
import schemas

router = APIRouter(prefix="/matching", tags=["Matching"])


@router.post("/", response_model=schemas.MatchRequestResponse, status_code=status.HTTP_201_CREATED)
def create_match_request(
    request: schemas.MatchRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["user"]))
):
    db_request = models.MatchRequest(
        user_id=current_user.id,
        province=request.province,
        need_type=request.need_type,
        message=request.message,
        status="pending"
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


@router.get("/my-requests", response_model=list[schemas.MatchRequestResponse])
def get_my_match_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["user"]))
):
    return (
        db.query(models.MatchRequest)
        .filter(models.MatchRequest.user_id == current_user.id)
        .all()
    )


@router.get("/all", response_model=list[schemas.MatchRequestResponse])
def get_all_match_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "supplier"]))
):
    return db.query(models.MatchRequest).all()