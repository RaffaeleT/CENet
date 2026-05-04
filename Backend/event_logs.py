from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth import get_db, get_current_user, require_role
import models
import schemas

router = APIRouter(prefix="/events", tags=["Event Logs"])


def log_event(
    db: Session,
    event_type: str,
    user_id: int | None = None,
    details: dict | None = None
):
    event = models.EventLog(
        event_type=event_type,
        user_id=user_id,
        details=details or {}
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.post("/", response_model=schemas.EventLogResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: schemas.EventLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return log_event(
        db=db,
        event_type=event_data.event_type,
        user_id=current_user.id,
        details=event_data.details
    )


@router.get("/my", response_model=list[schemas.EventLogResponse])
def get_my_events(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.EventLog)
        .filter(models.EventLog.user_id == current_user.id)
        .order_by(models.EventLog.created_at.desc())
        .all()
    )


@router.get("/all", response_model=list[schemas.EventLogResponse])
def get_all_events(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "supplier"]))
):
    return (
        db.query(models.EventLog)
        .order_by(models.EventLog.created_at.desc())
        .all()
    )