from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import get_db, get_current_user, require_role
import models
import schemas


router = APIRouter(prefix="/event-logs", tags=["Event Logs"])


def log_event(
    db: Session,
    event_type: str,
    user_id: int | None = None,
    details: dict | None = None,
):
    event = models.EventLog(
        event_type=event_type,
        user_id=user_id,
        details=details or {},
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.post("/", response_model=schemas.EventLogResponse)
def create_event_log(
    event: schemas.EventLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return log_event(
        db=db,
        event_type=event.event_type,
        user_id=current_user.id,
        details=event.details,
    )


@router.get("/", response_model=list[schemas.EventLogResponse])
def get_event_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"])),
):
    return (
        db.query(models.EventLog)
        .order_by(models.EventLog.created_at.desc())
        .limit(100)
        .all()
    )