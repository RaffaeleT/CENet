import io
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from auth import get_db, require_role
from event_logs import log_event
import models
import schemas

router = APIRouter(prefix="/rec-energy", tags=["REC Energy Data"])

REQUIRED_COLUMNS = {
    "date",
    "pod_id",
    "kwh_produced",
    "kwh_consumed",
    "kwh_shared"
}


def read_energy_file(file: UploadFile) -> pd.DataFrame:
    content = file.file.read()

    if file.filename.lower().endswith(".csv"):
        return pd.read_csv(io.BytesIO(content))

    if file.filename.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(content))

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Only CSV and Excel files are supported"
    )


def validate_energy_dataframe(df: pd.DataFrame):
    errors = []

    normalized_columns = {col: col.strip().lower() for col in df.columns}
    df.rename(columns=normalized_columns, inplace=True)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        errors.append({
            "type": "missing_columns",
            "columns": list(missing_columns)
        })
        return errors, None, None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if df["date"].isna().any():
        errors.append({
            "type": "invalid_dates",
            "message": "One or more rows contain invalid dates."
        })

    for col in ["kwh_produced", "kwh_consumed", "kwh_shared"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

        if df[col].isna().any():
            errors.append({
                "type": "invalid_numeric_values",
                "column": col
            })

        if (df[col] < 0).any():
            errors.append({
                "type": "negative_values",
                "column": col
            })

    if df["pod_id"].isna().any():
        errors.append({
            "type": "missing_pod_id",
            "message": "One or more rows are missing POD ID."
        })

    period_start = df["date"].min().to_pydatetime() if not df["date"].isna().all() else None
    period_end = df["date"].max().to_pydatetime() if not df["date"].isna().all() else None

    return errors, period_start, period_end


def get_owned_community(db: Session, community_id: int, current_user: models.User):
    if current_user.role == "admin":
        community = (
            db.query(models.EnergyCommunity)
            .filter(models.EnergyCommunity.id == community_id)
            .first()
        )
    else:
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


@router.post(
    "/{community_id}/upload",
    response_model=schemas.RECEnergyUploadResponse,
    status_code=status.HTTP_201_CREATED
)
def upload_rec_energy_file(
    community_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    df = read_energy_file(file)
    errors, period_start, period_end = validate_energy_dataframe(df)

    upload = models.RECEnergyUpload(
        community_id=community_id,
        uploaded_by=current_user.id,
        filename=file.filename,
        file_type=file.filename.split(".")[-1].lower(),
        period_start=period_start,
        period_end=period_end,
        status="failed" if errors else "validated",
        validation_errors={"errors": errors} if errors else None
    )

    db.add(upload)
    db.commit()
    db.refresh(upload)

    if errors:
        log_event(
            db=db,
            event_type="rec_energy_upload_failed",
            user_id=current_user.id,
            details={
                "community_id": community_id,
                "upload_id": upload.id,
                "errors": errors
            }
        )
        return upload

    if period_start and period_end:
        (
            db.query(models.RECEnergyReading)
            .filter(
                models.RECEnergyReading.community_id == community_id,
                models.RECEnergyReading.reading_date >= period_start,
                models.RECEnergyReading.reading_date <= period_end
            )
            .delete(synchronize_session=False)
        )

    readings = []

    for _, row in df.iterrows():
        readings.append(
            models.RECEnergyReading(
                community_id=community_id,
                upload_id=upload.id,
                pod_id=str(row["pod_id"]),
                reading_date=row["date"].to_pydatetime(),
                kwh_produced=float(row["kwh_produced"]),
                kwh_consumed=float(row["kwh_consumed"]),
                kwh_shared=float(row["kwh_shared"])
            )
        )

    db.add_all(readings)
    db.commit()

    log_event(
        db=db,
        event_type="rec_energy_uploaded",
        user_id=current_user.id,
        details={
            "community_id": community_id,
            "upload_id": upload.id,
            "rows": len(readings),
            "period_start": period_start.isoformat() if period_start else None,
            "period_end": period_end.isoformat() if period_end else None
        }
    )

    return upload


@router.get("/{community_id}/uploads", response_model=list[schemas.RECEnergyUploadResponse])
def get_rec_upload_history(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    return (
        db.query(models.RECEnergyUpload)
        .filter(models.RECEnergyUpload.community_id == community_id)
        .order_by(models.RECEnergyUpload.created_at.desc())
        .all()
    )


@router.get("/{community_id}/kpis", response_model=schemas.RECKPIResponse)
def get_rec_kpis(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    totals = (
        db.query(
            func.coalesce(func.sum(models.RECEnergyReading.kwh_produced), 0),
            func.coalesce(func.sum(models.RECEnergyReading.kwh_consumed), 0),
            func.coalesce(func.sum(models.RECEnergyReading.kwh_shared), 0),
        )
        .filter(models.RECEnergyReading.community_id == community_id)
        .first()
    )

    produced, consumed, shared = totals
    self_consumption_percentage = round((shared / produced) * 100, 2) if produced > 0 else 0

    return {
        "community_id": community_id,
        "total_produced_kwh": round(produced, 2),
        "total_consumed_kwh": round(consumed, 2),
        "total_shared_kwh": round(shared, 2),
        "self_consumption_percentage": self_consumption_percentage
    }


@router.get("/{community_id}/trends", response_model=list[schemas.RECTrendResponse])
def get_rec_trends(
    community_id: int,
    period: str = "monthly",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    if period == "yearly":
        group_fields = [extract("year", models.RECEnergyReading.reading_date)]
    elif period == "quarterly":
        group_fields = [
            extract("year", models.RECEnergyReading.reading_date),
            extract("quarter", models.RECEnergyReading.reading_date)
        ]
    else:
        group_fields = [
            extract("year", models.RECEnergyReading.reading_date),
            extract("month", models.RECEnergyReading.reading_date)
        ]

    rows = (
        db.query(
            *group_fields,
            func.sum(models.RECEnergyReading.kwh_produced),
            func.sum(models.RECEnergyReading.kwh_consumed),
            func.sum(models.RECEnergyReading.kwh_shared)
        )
        .filter(models.RECEnergyReading.community_id == community_id)
        .group_by(*group_fields)
        .all()
    )

    result = []

    for row in rows:
        *period_values, produced, consumed, shared = row
        period_label = "-".join(str(int(value)) for value in period_values)

        result.append({
            "period": period_label,
            "produced_kwh": round(produced or 0, 2),
            "consumed_kwh": round(consumed or 0, 2),
            "shared_kwh": round(shared or 0, 2)
        })

    return result


@router.get("/{community_id}/members", response_model=list[schemas.RECMemberEnergyResponse])
def get_rec_member_energy(
    community_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(["operator", "admin"]))
):
    get_owned_community(db, community_id, current_user)

    rows = (
        db.query(
            models.RECEnergyReading.pod_id,
            func.sum(models.RECEnergyReading.kwh_produced),
            func.sum(models.RECEnergyReading.kwh_consumed),
            func.sum(models.RECEnergyReading.kwh_shared)
        )
        .filter(models.RECEnergyReading.community_id == community_id)
        .group_by(models.RECEnergyReading.pod_id)
        .all()
    )

    return [
        {
            "pod_id": pod_id,
            "produced_kwh": round(produced or 0, 2),
            "consumed_kwh": round(consumed or 0, 2),
            "shared_kwh": round(shared or 0, 2)
        }
        for pod_id, produced, consumed, shared in rows
    ]