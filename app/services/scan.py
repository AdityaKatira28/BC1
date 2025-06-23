from datetime import datetime
from app.models import ScanResult, ComplianceCheck

def perform_scan(records: list[ComplianceCheck]) -> ScanResult:
    failures = [r for r in records if r.status != r.StatusLevel.PASSING]
    return ScanResult(results=failures, scanned_at=datetime.utcnow())