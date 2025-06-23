from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List, Optional
from app.config import settings
from app.models import (
    ComplianceCheck, DashboardSummary, AiInsights,
    ScanResult, DetailedStatistics, StatusLevel, SeverityLevel
)
from app.utils import parse_and_validate_csv
from app.services.dashboard import compute_dashboard
from app.services.scan import perform_scan
from app.services.statistics import compute_statistics
from app.ai_model import AIModel
from app.mock_data import get_mock_compliance_checks, get_mock_dashboard_summary, get_mock_ai_insights
from app.data_store import data_store
from datetime import datetime

router = APIRouter(prefix="/api/v1")
_ai = AIModel(settings.model_path)

@router.post("/upload", response_model=dict, tags=["Data"])
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only CSV files supported")
    content = await file.read()
    records = parse_and_validate_csv(content)
    data_store.set_data(records)
    return {"message": f"Loaded {len(records)} records"}

@router.get("/dashboard", response_model=DashboardSummary, tags=["Metrics"])
def dashboard():
    if data_store.is_empty():
        # Return mock data when no real data is uploaded
        return get_mock_dashboard_summary()
    return compute_dashboard(data_store.get_data())

@router.get("/ai-insights", response_model=AiInsights, tags=["AI"])
def ai_insights():
    if data_store.is_empty():
        # Return mock AI insights when no real data is uploaded
        return get_mock_ai_insights()
    violations = [c.dict() for c in data_store.get_data() if c.status != StatusLevel.PASSING]
    return _ai.generate_insights(violations)

@router.get("/checks", response_model=List[ComplianceCheck], tags=["Data"])
def list_checks(
    framework: Optional[str] = Query(None),
    provider: Optional[str]  = Query(None),
    severity: Optional[str]  = Query(None),
    status:   Optional[str]  = Query(None),
    limit:    int            = Query(100)
):
    # Use persistent data if available, otherwise mock data
    data_source = data_store.get_data() if not data_store.is_empty() else get_mock_compliance_checks()
    res = data_source
    
    if framework: res = [r for r in res if r.framework == framework]
    if provider:  res = [r for r in res if r.provider == provider]
    if severity:  res = [r for r in res if r.severity.value == severity]
    if status:    res = [r for r in res if r.status.value == status]
    return res[:limit]

@router.get("/frameworks", tags=["Data"])
def frameworks():
    data_source = data_store.get_data() if not data_store.is_empty() else get_mock_compliance_checks()
    return {"frameworks": sorted({r.framework for r in data_source})}

@router.get("/providers", tags=["Data"])
def providers():
    data_source = data_store.get_data() if not data_store.is_empty() else get_mock_compliance_checks()
    return {"providers": sorted({r.provider for r in data_source})}

@router.post("/scan", response_model=ScanResult, tags=["Data"])
def scan():
    if data_store.is_empty():
        # Return mock scan result when no real data is uploaded
        mock_checks = get_mock_compliance_checks()
        return ScanResult(
            results=mock_checks[:10],  # Return first 10 as scan results
            scanned_at=datetime.now()
        )
    return perform_scan(data_store.get_data())

@router.get("/statistics", response_model=DetailedStatistics, tags=["Analytics"])
def statistics():
    if data_store.is_empty():
        # Return mock statistics when no real data is uploaded
        mock_checks = get_mock_compliance_checks()
        return compute_statistics(mock_checks)
    return compute_statistics(data_store.get_data())

@router.delete("/data", tags=["Data"])
def clear_data():
    """Clear all uploaded data and return to mock data"""
    data_store.clear_data()
    return {"message": "All data cleared, returning to mock data"}

@router.get("/data/status", tags=["Data"])
def data_status():
    """Get information about current data status"""
    if data_store.is_empty():
        return {
            "status": "mock_data",
            "message": "Using mock data - no real data uploaded",
            "record_count": 0
        }
    else:
        return {
            "status": "real_data", 
            "message": "Using uploaded real data",
            "record_count": len(data_store.get_data())
        }