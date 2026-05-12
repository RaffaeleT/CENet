from datetime import datetime
from sqlalchemy.orm import Session

import models


def log_error(
    db: Session,
    endpoint: str,
    error_type: str,
    error_message: str | None = None,
    user_id: int | None = None,
    module: str | None = None
):
    error_log = models.ErrorLog(
        user_id=user_id,
        module=module,
        endpoint=endpoint,
        error_type=error_type,
        error_message=error_message,
        timestamp=datetime.utcnow()
    )

    db.add(error_log)
    db.commit()
    db.refresh(error_log)

    return error_log


def log_api_performance(
    db: Session,
    endpoint: str,
    method: str,
    status_code: int,
    response_time: float
):
    performance_log = models.APIPerformanceLog(
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        response_time=response_time,
        timestamp=datetime.utcnow()
    )

    db.add(performance_log)
    db.commit()
    db.refresh(performance_log)

    return performance_log