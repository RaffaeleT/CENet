import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth import get_db, require_role
from event_logs import log_event
import models
import schemas

router = APIRouter(prefix="/newsletter", tags=["Newsletter"])


@router.post("/subscribe", response_model=schemas.NewsletterSubscriberResponse, status_code=status.HTTP_201_CREATED)
def subscribe_newsletter(
    subscriber: schemas.NewsletterSubscribeCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(models.NewsletterSubscriber)
        .filter(models.NewsletterSubscriber.email == subscriber.email)
        .first()
    )

    if existing:
        existing.is_active = True
        existing.name = subscriber.name or existing.name
        existing.user_type = subscriber.user_type or existing.user_type
        existing.preferences = subscriber.preferences or existing.preferences
        existing.unsubscribed_at = None

        db.commit()
        db.refresh(existing)

        return existing

    db_subscriber = models.NewsletterSubscriber(
        name=subscriber.name,
        email=subscriber.email,
        user_type=subscriber.user_type,
        preferences=subscriber.preferences or {},
        unsubscribe_token=str(uuid.uuid4())
    )

    try:
        db.add(db_subscriber)
        db.commit()
        db.refresh(db_subscriber)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not subscribe email")

    log_event(
        db=db,
        event_type="newsletter_subscribed",
        user_id=None,
        details={
            "subscriber_id": db_subscriber.id,
            "email": db_subscriber.email,
            "user_type": db_subscriber.user_type,
            "preferences": db_subscriber.preferences
        }
    )

    return db_subscriber


@router.put("/unsubscribe/{token}")
def unsubscribe_newsletter(
    token: str,
    db: Session = Depends(get_db)
):
    subscriber = (
        db.query(models.NewsletterSubscriber)
        .filter(models.NewsletterSubscriber.unsubscribe_token == token)
        .first()
    )

    if subscriber is None:
        raise HTTPException(status_code=404, detail="Invalid unsubscribe token")

    subscriber.is_active = False
    subscriber.unsubscribed_at = datetime.utcnow()

    db.commit()
    db.refresh(subscriber)

    return {"message": "Successfully unsubscribed"}


@router.get("/subscribers", response_model=list[schemas.NewsletterSubscriberResponse])
def get_newsletter_subscribers(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["admin"]))
):
    return (
        db.query(models.NewsletterSubscriber)
        .order_by(models.NewsletterSubscriber.created_at.desc())
        .all()
    )