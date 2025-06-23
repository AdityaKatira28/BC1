from itertools import groupby
from typing import List
from app.models import ComplianceCheck, DashboardSummary, StatusLevel, SeverityLevel

def compute_dashboard(records: List[ComplianceCheck]) -> DashboardSummary:
    total = len(records)
    compliant = sum(r.status == StatusLevel.PASSING for r in records)
    non_compliant = total - compliant
    critical_count = sum(r.severity == SeverityLevel.CRITICAL for r in records)

    # Calculate framework scores (average risk score per framework)
    framework_groups = {}
    for record in records:
        if record.framework not in framework_groups:
            framework_groups[record.framework] = []
        framework_groups[record.framework].append(record.risk_score)
    
    framework_scores = {
        fw: round(sum(scores) / len(scores), 2)
        for fw, scores in framework_groups.items()
    }

    # Calculate provider stats
    provider_groups = {}
    for record in records:
        if record.provider not in provider_groups:
            provider_groups[record.provider] = []
        provider_groups[record.provider].append(record)
    
    provider_stats = {}
    for prov, recs in provider_groups.items():
        critical_issues = sum(1 for r in recs if r.severity == SeverityLevel.CRITICAL and r.status != StatusLevel.PASSING)
        provider_stats[prov] = {
            "total": len(recs),
            "critical": critical_issues
        }

    # Get recent violations (non-passing checks)
    recent_violations = sorted(
        [r for r in records if r.status != StatusLevel.PASSING],
        key=lambda x: x.last_checked, reverse=True
    )[:10]  # Get top 10 recent violations

    return DashboardSummary(
        total_checks=total,
        compliant=compliant,
        non_compliant=non_compliant,
        critical_count=critical_count,
        framework_scores=framework_scores,
        provider_stats=provider_stats,
        recent_violations=recent_violations
    )

