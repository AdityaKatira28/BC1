import pandas as pd
import uuid
from fastapi import HTTPException
from app.models import ComplianceCheck

REQUIRED_COLUMNS = {
    "framework", "provider", "severity", "status",
    "risk_score", "description", "last_checked"
}

def parse_and_validate_csv(content: bytes) -> list[ComplianceCheck]:
    try:
        df = pd.read_csv(pd.io.common.BytesIO(content))
    except Exception as e:
        raise HTTPException(400, f"Invalid CSV format: {e}")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise HTTPException(400, detail=f"Missing columns: {missing}")

    df["last_checked"] = pd.to_datetime(df["last_checked"], errors="raise")
    if "id" not in df.columns:
        df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    records = df.to_dict(orient="records")
    return [ComplianceCheck(**r) for r in records]