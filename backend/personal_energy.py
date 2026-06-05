import io

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from auth import get_db, get_current_user
from event_logs import log_event
import models
import schemas

router = APIRouter(prefix="/personal-energy", tags=["Personal Energy Data"])

REQUIRED_COLUMNS = {
    "date",
    "kwh_consumed",
    "kwh_produced",
    "kwh_fed_to_grid",
    "kwh_self_consumed"
}


def read_file(file: UploadFile) -> pd.DataFrame:
    content = file.file.read()

    if file.filename.lower().endswith(".csv"):
        return pd.read_csv(io.BytesIO(content))

    if file.filename.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(content))

    raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported")


def validate_dataframe(df: pd.DataFrame):
    errors = []

    normalized_columns = {col: col.strip().lower() for col in df.columns}
    df.rename(columns=normalized_columns, inplace=True)

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        errors.append({"type": "missing_columns", "columns": list(missing_columns)})
        return errors, None, None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if df["date"].isna().any():
        errors.append({"type": "invalid_dates"})

    for col in ["kwh_consumed", "kwh_produced", "kwh_fed_to_grid", "kwh_self_consumed"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

        if df[col].isna().any():
            errors.append({"type": "invalid_numeric_values", "column": col})

        if (df[col] < 0).any():
            errors.append({"type": "negative_values", "column": col})

    period_start = df["date"].min().to_pydatetime() if not df["date"].isna().all() else None
    period_end = df["date"].max().to_pydatetime() if not df["date"].isna().all() else None

    return errors, period_start, period_end


@router.post("/upload", response_model=schemas.PersonalEnergyUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_personal_energy_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    df = read_file(file)
    errors, period_start, period_end = validate_dataframe(df)

    upload = models.PersonalEnergyUpload(
        user_id=current_user.id,
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
            event_type="personal_energy_upload_failed",
            user_id=current_user.id,
            details={"upload_id": upload.id, "errors": errors}
        )
        return upload

    if period_start and period_end:
        (
            db.query(models.PersonalEnergyReading)
            .filter(
                models.PersonalEnergyReading.user_id == current_user.id,
                models.PersonalEnergyReading.reading_date >= period_start,
                models.PersonalEnergyReading.reading_date <= period_end
            )
            .delete(synchronize_session=False)
        )

    readings = []

    for _, row in df.iterrows():
        readings.append(
            models.PersonalEnergyReading(
                user_id=current_user.id,
                upload_id=upload.id,
                pod_id=str(row["pod_id"]) if "pod_id" in df.columns else None,
                reading_date=row["date"].to_pydatetime(),
                kwh_consumed=float(row["kwh_consumed"]),
                kwh_produced=float(row["kwh_produced"]),
                kwh_fed_to_grid=float(row["kwh_fed_to_grid"]),
                kwh_self_consumed=float(row["kwh_self_consumed"])
            )
        )

    db.add_all(readings)
    db.commit()

    log_event(
        db=db,
        event_type="personal_energy_uploaded",
        user_id=current_user.id,
        details={"upload_id": upload.id, "rows": len(readings)}
    )

    return upload


@router.post("/manual", response_model=schemas.ManualEnergyInputResponse, status_code=status.HTTP_201_CREATED)
def create_manual_energy_input(
    manual_input: schemas.ManualEnergyInputCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_input = models.ManualEnergyInput(
        user_id=current_user.id,
        annual_consumption_kwh=manual_input.annual_consumption_kwh,
        system_power_kw=manual_input.system_power_kw,
        province=manual_input.province
    )

    db.add(db_input)
    db.commit()
    db.refresh(db_input)

    log_event(
        db=db,
        event_type="manual_energy_input_created",
        user_id=current_user.id,
        details={
            "manual_input_id": db_input.id,
            "annual_consumption_kwh": db_input.annual_consumption_kwh,
            "system_power_kw": db_input.system_power_kw
        }
    )

    return db_input


@router.get("/uploads", response_model=list[schemas.PersonalEnergyUploadResponse])
def get_personal_upload_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return (
        db.query(models.PersonalEnergyUpload)
        .filter(models.PersonalEnergyUpload.user_id == current_user.id)
        .order_by(models.PersonalEnergyUpload.created_at.desc())
        .all()
    )


@router.get("/kpis", response_model=schemas.PersonalKPIResponse)
def get_personal_kpis(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    totals = (
        db.query(
            func.coalesce(func.sum(models.PersonalEnergyReading.kwh_consumed), 0),
            func.coalesce(func.sum(models.PersonalEnergyReading.kwh_produced), 0),
            func.coalesce(func.sum(models.PersonalEnergyReading.kwh_fed_to_grid), 0),
            func.coalesce(func.sum(models.PersonalEnergyReading.kwh_self_consumed), 0),
        )
        .filter(models.PersonalEnergyReading.user_id == current_user.id)
        .first()
    )

    consumed, produced, fed_to_grid, self_consumed = totals

    months_count = (
        db.query(
            extract("year", models.PersonalEnergyReading.reading_date),
            extract("month", models.PersonalEnergyReading.reading_date)
        )
        .filter(models.PersonalEnergyReading.user_id == current_user.id)
        .group_by(
            extract("year", models.PersonalEnergyReading.reading_date),
            extract("month", models.PersonalEnergyReading.reading_date)
        )
        .count()
    )

    average_monthly = round(consumed / months_count, 2) if months_count > 0 else 0
    self_consumption_percentage = round((self_consumed / produced) * 100, 2) if produced > 0 else 0

    return {
        "user_id": current_user.id,
        "total_consumed_kwh": round(consumed, 2),
        "total_produced_kwh": round(produced, 2),
        "total_fed_to_grid_kwh": round(fed_to_grid, 2),
        "total_self_consumed_kwh": round(self_consumed, 2),
        "average_monthly_consumption_kwh": average_monthly,
        "self_consumption_percentage": self_consumption_percentage
    }