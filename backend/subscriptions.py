from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_db, require_role
from event_logs import log_event
import models
import schemas

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

CENET_CONTACT_EMAIL = "connect@cenet.it"


@router.post(
    "/contact",
    response_model=schemas.SubscriptionContactResponse,
    status_code=status.HTTP_201_CREATED
)
def create_subscription_contact(
    contact: schemas.SubscriptionContactCreate,
    db: Session = Depends(get_db)
):
    db_contact = models.SubscriptionContact(
        email=contact.email,
        name=contact.name,
        message=contact.message,
        source=contact.source or "website",
        status="new"
    )

    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)

    log_event(
        db=db,
        event_type="subscription_contact_created",
        user_id=None,
        details={
            "contact_id": db_contact.id,
            "email": db_contact.email,
            "name": db_contact.name,
            "source": db_contact.source,
            "status": db_contact.status
        }
    )

    return db_contact


@router.get("/contact", response_model=list[schemas.SubscriptionContactResponse])
def get_subscription_contacts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return (
        db.query(models.SubscriptionContact)
        .order_by(models.SubscriptionContact.created_at.desc())
        .all()
    )


@router.get("/contact/{contact_id}", response_model=schemas.SubscriptionContactResponse)
def get_subscription_contact_by_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    contact = (
        db.query(models.SubscriptionContact)
        .filter(models.SubscriptionContact.id == contact_id)
        .first()
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription/contact request not found"
        )

    return contact


@router.put("/contact/{contact_id}", response_model=schemas.SubscriptionContactResponse)
def update_subscription_contact_status(
    contact_id: int,
    contact_update: schemas.SubscriptionContactUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    contact = (
        db.query(models.SubscriptionContact)
        .filter(models.SubscriptionContact.id == contact_id)
        .first()
    )

    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription/contact request not found"
        )

    contact.status = contact_update.status
    db.commit()
    db.refresh(contact)

    log_event(
        db=db,
        event_type="subscription_contact_status_updated",
        user_id=current_user.id,
        details={
            "contact_id": contact.id,
            "email": contact.email,
            "new_status": contact.status
        }
    )

    return contact


@router.get("/info")
def get_subscription_info():
    return {
        "contact_email": CENET_CONTACT_EMAIL,
        "message": "For subscription or partnership inquiries, please contact connect@cenet.it."
    }