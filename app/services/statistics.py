from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List

from app.models import ComplianceCheck, DetailedStatistics

def compute_statistics(records: List[ComplianceCheck]) -> DetailedStatistics:
    now = datetime.utcnow()
    total = len(records)
    avg_risk = round(sum(r.risk_score for r in records) / total, 2) if total else 0.0

    # Overview
    overview = {
        "total_checks": total,
        "avg_risk_score": avg_risk,
        "critical_violations": sum(r.severity == r.SeverityLevel.CRITICAL for r in records),
        "last_updated": now.isoformat()
    }

    # By severity
    by_severity = {
        level.value: sum(r.severity.value == level.value for r in records)
        for level in ComplianceCheck.__fields__['severity'].type_.__members__.values()
    }

    # By framework & provider
    def make_group(key_fn):
        grp: dict[str, int] = defaultdict(int)
        for r in records:
            grp[key_fn(r)] += 1
        return dict(grp)

    by_framework = make_group(lambda r: r.framework)
    by_provider  = make_group(lambda r: r.provider)

    # By status
    by_status = Counter(r.status.value for r in records)

    # Trends: count per day over last 7 days
    trends_counter: Counter[str] = Counter()
    week_ago = now - timedelta(days=7)
    for r in records:
        if r.last_checked >= week_ago:
            date_str = r.last_checked.date().isoformat()
            trends_counter[date_str] += 1
    trends = dict(trends_counter)

    return DetailedStatistics(
        overview=overview,
        by_severity=by_severity,
        by_framework={k: {"count": v} for k, v in by_framework.items()},
        by_provider={k: {"count": v} for k, v in by_provider.items()},
        by_status=dict(by_status),
        trends=trends
    )