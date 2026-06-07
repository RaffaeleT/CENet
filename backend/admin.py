from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import get_db, require_role
import models
import schemas

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=schemas.AdminDashboardResponse)
def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return {
        "total_users": db.query(models.User).count(),
        "total_communities": db.query(models.EnergyCommunity).count(),
        "total_match_requests": db.query(models.MatchRequest).count(),
        "total_simulations": db.query(models.Simulation).count(),
        "total_suppliers": db.query(models.Supplier).count(),
        "total_contact_requests": db.query(models.ContactRequest).count(),
        "total_events": db.query(models.EventLog).count(),
        "total_errors": db.query(models.ErrorLog).count(),
        "total_api_logs": db.query(models.APIPerformanceLog).count()
    }


@router.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return db.query(models.User).order_by(models.User.id.desc()).all()


@router.get("/events", response_model=list[schemas.EventLogResponse])
def get_admin_events(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return (
        db.query(models.EventLog)
        .order_by(models.EventLog.created_at.desc())
        .limit(100)
        .all()
    )

@router.get("/errors", response_model=list[schemas.ErrorLogResponse])
def get_error_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return (
        db.query(models.ErrorLog)
        .order_by(models.ErrorLog.timestamp.desc())
        .limit(100)
        .all()
    )


@router.get("/performance", response_model=list[schemas.APIPerformanceLogResponse])
def get_api_performance_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return (
        db.query(models.APIPerformanceLog)
        .order_by(models.APIPerformanceLog.timestamp.desc())
        .limit(100)
        .all()
    )