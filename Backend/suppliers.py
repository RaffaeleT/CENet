from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import get_db, require_role
import models
import schemas

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


@router.get("/", response_model=list[schemas.SupplierResponse])
def get_suppliers(
    category: Optional[str] = None,
    province: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Supplier)

    if category:
        query = query.filter(models.Supplier.category == category)

    if province:
        query = query.filter(models.Supplier.province == province)

    return query.all()


@router.get("/{supplier_id}", response_model=schemas.SupplierResponse)
def get_supplier_by_id(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return supplier


@router.post("/", response_model=schemas.SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier: schemas.SupplierCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["supplier"]))
):
    db_supplier = models.Supplier(
        name=supplier.name,
        category=supplier.category,
        province=supplier.province,
        description=supplier.description,
        verified=supplier.verified,
        plan_tier=supplier.plan_tier
    )

    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)

    return db_supplier


@router.post("/contact", response_model=schemas.ContactRequestResponse, status_code=status.HTTP_201_CREATED)
def create_contact_request(
    request: schemas.ContactRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["user", "operator"]))
):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == request.supplier_id).first()

    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db_request = models.ContactRequest(
        user_id=current_user.id,
        supplier_id=request.supplier_id,
        message=request.message,
        status="pending"
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return db_request


@router.get("/leads", response_model=list[schemas.ContactRequestResponse])
def get_supplier_leads(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["supplier"]))
):
    return db.query(models.ContactRequest).order_by(models.ContactRequest.created_at.desc()).all()


@router.put("/leads/{lead_id}", response_model=schemas.ContactRequestResponse)
def update_lead_status(
    lead_id: int,
    lead_update: schemas.ContactRequestUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["supplier"]))
):
    lead = db.query(models.ContactRequest).filter(models.ContactRequest.id == lead_id).first()

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.status = lead_update.status
    db.commit()
    db.refresh(lead)

    return lead