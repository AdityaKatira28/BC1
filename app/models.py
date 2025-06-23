from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class SeverityLevel(str, Enum):
    CRITICAL = "Critical"
    HIGH     = "High"
    MEDIUM   = "Medium"
    LOW      = "Low"

class StatusLevel(str, Enum):
    PASSING  = "Passing"
    FAILING  = "Failing"
    WARNING  = "Warning"

class ComplianceCheck(BaseModel):
    id: str
    framework: str
    provider: str
    severity: SeverityLevel
    status: StatusLevel
    risk_score: float = Field(..., ge=0.0, le=10.0)
    description: str
    last_checked: datetime
    ai_summary: Optional[str] = None

class DashboardSummary(BaseModel):
    total_checks: int
    compliant: int
    non_compliant: int
    critical_count: int
    framework_scores: Dict[str, float]
    provider_stats: Dict[str, Dict[str, int]]
    recent_violations: List[ComplianceCheck]

class AiInsights(BaseModel):
    summary: Dict[str, int | str]
    recommendations: List[Dict[str, str]]

class ScanResult(BaseModel):
    results: List[ComplianceCheck]
    scanned_at: datetime

class DetailedStatistics(BaseModel):
    overview: Dict[str, float]
    by_severity: Dict[str, Dict[str, int]]
    by_framework: Dict[str, Dict[str, int]]
    by_provider: Dict[str, Dict[str, int]]
    by_status: Dict[str, int]
    trends: Dict[str, int]