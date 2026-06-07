from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_db, require_role
from event_logs import log_event
import models
import schemas

router = APIRouter(prefix="/communities", tags=["Communities"])


def get_owned_community_or_404(
    community_id: int,
    db: Session,
    current_user: models.User
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Community not found"
        )

    return community


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

    log_event(
        db=db,
        event_type="community_created",
        user_id=current_user.id,
        details={
            "community_id": db_community.id,
            "name": db_community.name,
            "province": db_community.province,
            "region": db_community.region,
            "status": db_community.status
        }
    )

    return db_community


@router.get("/my", response_model=list[schemas.EnergyCommunityResponse])
def get_my_communities(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    return (
        db.query(models.EnergyCommunity)
        .filter(models.EnergyCommunity.manager_id == current_user.id)
        .order_by(models.EnergyCommunity.created_at.desc())
        .all()
    )


@router.get("/{community_id}", response_model=schemas.EnergyCommunityResponse)
def get_community(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    return get_owned_community_or_404(
        community_id=community_id,
        db=db,
        current_user=current_user
    )


@router.put("/{community_id}", response_model=schemas.EnergyCommunityResponse)
def update_community(
    community_id: int,
    community_update: schemas.EnergyCommunityUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    community = get_owned_community_or_404(
        community_id=community_id,
        db=db,
        current_user=current_user
    )

    update_data = community_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(community, field, value)

    db.commit()
    db.refresh(community)

    log_event(
        db=db,
        event_type="community_updated",
        user_id=current_user.id,
        details={
            "community_id": community.id,
            "updated_fields": list(update_data.keys())
        }
    )

    return community


@router.delete("/{community_id}")
def delete_community(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    community = get_owned_community_or_404(
        community_id=community_id,
        db=db,
        current_user=current_user
    )

    community_name = community.name

    db.delete(community)
    db.commit()

    log_event(
        db=db,
        event_type="community_deleted",
        user_id=current_user.id,
        details={
            "community_id": community_id,
            "name": community_name
        }
    )

    return {"message": "Community deleted successfully"}


@router.post(
    "/{community_id}/members",
    response_model=schemas.CommunityMemberResponse,
    status_code=status.HTTP_201_CREATED
)
def add_community_member(
    community_id: int,
    member: schemas.CommunityMemberCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    community = get_owned_community_or_404(
        community_id=community_id,
        db=db,
        current_user=current_user
    )

    user = db.query(models.User).filter(models.User.id == member.user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    existing_member = (
        db.query(models.CommunityMember)
        .filter(
            models.CommunityMember.community_id == community_id,
            models.CommunityMember.user_id == member.user_id
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this community"
        )

    db_member = models.CommunityMember(
        community_id=community.id,
        user_id=member.user_id,
        member_role=member.member_role,
        pod_id=member.pod_id,
        status=member.status
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    log_event(
        db=db,
        event_type="community_member_added",
        user_id=current_user.id,
        details={
            "community_id": community.id,
            "member_user_id": member.user_id,
            "member_role": member.member_role,
            "status": member.status
        }
    )

    return db_member


@router.get("/{community_id}/members", response_model=list[schemas.CommunityMemberResponse])
def get_community_members(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    get_owned_community_or_404(
        community_id=community_id,
        db=db,
        current_user=current_user
    )

    return (
        db.query(models.CommunityMember)
        .filter(models.CommunityMember.community_id == community_id)
        .order_by(models.CommunityMember.joined_at.desc())
        .all()
    )


@router.put("/{community_id}/members/{member_id}", response_model=schemas.CommunityMemberResponse)
def update_community_member(
    community_id: int,
    member_id: int,
    member_update: schemas.CommunityMemberUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    get_owned_community_or_404(
        community_id=community_id,
        db=db,
        current_user=current_user
    )

    db_member = (
        db.query(models.CommunityMember)
        .filter(
            models.CommunityMember.id == member_id,
            models.CommunityMember.community_id == community_id
        )
        .first()
    )

    if db_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    update_data = member_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_member, field, value)

    db.commit()
    db.refresh(db_member)

    log_event(
        db=db,
        event_type="community_member_updated",
        user_id=current_user.id,
        details={
            "community_id": community_id,
            "member_id": member_id,
            "updated_fields": list(update_data.keys())
        }
    )

    return db_member


@router.delete("/{community_id}/members/{member_id}")
def remove_community_member(
    community_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    get_owned_community_or_404(
        community_id=community_id,
        db=db,
        current_user=current_user
    )

    db_member = (
        db.query(models.CommunityMember)
        .filter(
            models.CommunityMember.id == member_id,
            models.CommunityMember.community_id == community_id
        )
        .first()
    )

    if db_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    member_user_id = db_member.user_id

    db.delete(db_member)
    db.commit()

    log_event(
        db=db,
        event_type="community_member_removed",
        user_id=current_user.id,
        details={
            "community_id": community_id,
            "member_id": member_id,
            "member_user_id": member_user_id
        }
    )

    return {"message": "Community member removed successfully"}


@router.get("/{community_id}/dashboard", response_model=schemas.CommunityDashboardResponse)
def get_community_dashboard(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator"]))
):
    community = get_owned_community_or_404(
        community_id=community_id,
        db=db,
        current_user=current_user
    )

    total_members = (
        db.query(models.CommunityMember)
        .filter(models.CommunityMember.community_id == community_id)
        .count()
    )

    active_members = (
        db.query(models.CommunityMember)
        .filter(
            models.CommunityMember.community_id == community_id,
            models.CommunityMember.status == "active"
        )
        .count()
    )

    invited_members = (
        db.query(models.CommunityMember)
        .filter(
            models.CommunityMember.community_id == community_id,
            models.CommunityMember.status == "invited"
        )
        .count()
    )

    inactive_members = (
        db.query(models.CommunityMember)
        .filter(
            models.CommunityMember.community_id == community_id,
            models.CommunityMember.status == "inactive"
        )
        .count()
    )

    events = (
        db.query(models.EventLog)
        .filter(models.EventLog.user_id == current_user.id)
        .order_by(models.EventLog.created_at.desc())
        .limit(10)
        .all()
    )

    recent_events = [
        {
            "id": event.id,
            "event_type": event.event_type,
            "details": event.details,
            "created_at": event.created_at.isoformat()
        }
        for event in events
    ]

    total_events = (
        db.query(models.EventLog)
        .filter(models.EventLog.user_id == current_user.id)
        .count()
    )

    return {
        "community_id": community.id,
        "community_name": community.name,
        "status": community.status,
        "province": community.province,
        "region": community.region,
        "total_members": total_members,
        "active_members": active_members,
        "invited_members": invited_members,
        "inactive_members": inactive_members,
        "total_events": total_events,
        "recent_events": recent_events
    }