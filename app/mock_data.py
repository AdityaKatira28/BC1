from datetime import datetime, timedelta
from app.models import ComplianceCheck, DashboardSummary, AiInsights, SeverityLevel, StatusLevel
from typing import List

def get_mock_compliance_checks() -> List[ComplianceCheck]:
    """Generate mock compliance check data"""
    base_time = datetime.now()
    
    mock_checks = [
        ComplianceCheck(
            id="cv-001",
            framework="SOC2",
            provider="AWS",
            severity=SeverityLevel.CRITICAL,
            status=StatusLevel.FAILING,
            risk_score=9.2,
            description="Unencrypted data transmission detected",
            last_checked=base_time - timedelta(hours=2),
            ai_summary="Critical security vulnerability: Data transmitted without encryption"
        ),
        ComplianceCheck(
            id="cv-002",
            framework="GDPR",
            provider="Azure",
            severity=SeverityLevel.HIGH,
            status=StatusLevel.FAILING,
            risk_score=7.8,
            description="Personal data retention policy violation",
            last_checked=base_time - timedelta(hours=4),
            ai_summary="Data retention exceeds GDPR requirements"
        ),
        ComplianceCheck(
            id="cv-003",
            framework="HIPAA",
            provider="GCP",
            severity=SeverityLevel.CRITICAL,
            status=StatusLevel.FAILING,
            risk_score=8.9,
            description="Healthcare data access logging insufficient",
            last_checked=base_time - timedelta(hours=1),
            ai_summary="Insufficient audit trails for healthcare data access"
        ),
        ComplianceCheck(
            id="cv-004",
            framework="PCI-DSS",
            provider="AWS",
            severity=SeverityLevel.MEDIUM,
            status=StatusLevel.WARNING,
            risk_score=5.2,
            description="Payment card data encryption needs review",
            last_checked=base_time - timedelta(hours=6),
            ai_summary="Payment data encryption configuration requires attention"
        ),
        ComplianceCheck(
            id="cv-005",
            framework="ISO27001",
            provider="Azure",
            severity=SeverityLevel.LOW,
            status=StatusLevel.PASSING,
            risk_score=2.1,
            description="Information security management system compliant",
            last_checked=base_time - timedelta(hours=3),
            ai_summary="ISMS implementation meets ISO27001 standards"
        ),
        # Add more mock data to reach realistic numbers
        ComplianceCheck(
            id="cv-006",
            framework="SOC2",
            provider="AWS",
            severity=SeverityLevel.LOW,
            status=StatusLevel.PASSING,
            risk_score=1.5,
            description="Access controls properly configured",
            last_checked=base_time - timedelta(hours=5),
            ai_summary="Access control mechanisms are functioning correctly"
        ),
        ComplianceCheck(
            id="cv-007",
            framework="GDPR",
            provider="GCP",
            severity=SeverityLevel.MEDIUM,
            status=StatusLevel.PASSING,
            risk_score=3.2,
            description="Data subject rights implementation verified",
            last_checked=base_time - timedelta(hours=8),
            ai_summary="Data subject rights processes are compliant"
        ),
        ComplianceCheck(
            id="cv-008",
            framework="HIPAA",
            provider="AWS",
            severity=SeverityLevel.HIGH,
            status=StatusLevel.WARNING,
            risk_score=6.7,
            description="Business associate agreements need update",
            last_checked=base_time - timedelta(hours=12),
            ai_summary="BAA documentation requires review and updates"
        ),
        ComplianceCheck(
            id="cv-009",
            framework="PCI-DSS",
            provider="Azure",
            severity=SeverityLevel.LOW,
            status=StatusLevel.PASSING,
            risk_score=2.8,
            description="Network security controls validated",
            last_checked=base_time - timedelta(hours=7),
            ai_summary="Network segmentation and security controls are adequate"
        ),
        ComplianceCheck(
            id="cv-010",
            framework="ISO27001",
            provider="GCP",
            severity=SeverityLevel.MEDIUM,
            status=StatusLevel.PASSING,
            risk_score=4.1,
            description="Risk assessment process documented",
            last_checked=base_time - timedelta(hours=9),
            ai_summary="Risk management processes meet ISO27001 requirements"
        )
    ]
    
    # Generate additional passing checks to reach realistic totals
    for i in range(11, 157):  # Generate up to 156 total checks
        mock_checks.append(
            ComplianceCheck(
                id=f"cv-{i:03d}",
                framework=["SOC2", "GDPR", "HIPAA", "PCI-DSS", "ISO27001"][i % 5],
                provider=["AWS", "Azure", "GCP"][i % 3],
                severity=[SeverityLevel.LOW, SeverityLevel.MEDIUM][i % 2],
                status=StatusLevel.PASSING,
                risk_score=round(1.0 + (i % 30) * 0.1, 1),
                description=f"Compliance check {i} - automated validation passed",
                last_checked=base_time - timedelta(hours=i % 24),
                ai_summary=f"Automated compliance check {i} completed successfully"
            )
        )
    
    return mock_checks

def get_mock_dashboard_summary() -> DashboardSummary:
    """Generate mock dashboard summary data"""
    checks = get_mock_compliance_checks()
    
    total_checks = len(checks)
    failing_checks = [c for c in checks if c.status == StatusLevel.FAILING]
    warning_checks = [c for c in checks if c.status == StatusLevel.WARNING]
    passing_checks = [c for c in checks if c.status == StatusLevel.PASSING]
    
    compliant = len(passing_checks)
    non_compliant = len(failing_checks) + len(warning_checks)
    critical_count = len([c for c in checks if c.severity == SeverityLevel.CRITICAL])
    
    # Calculate framework scores
    framework_scores = {
        "SOC2": 85.2,
        "GDPR": 92.1,
        "HIPAA": 78.9,
        "PCI-DSS": 88.7,
        "ISO27001": 91.3
    }
    
    # Calculate provider stats
    provider_stats = {}
    for provider in ["AWS", "Azure", "GCP"]:
        provider_checks = [c for c in checks if c.provider == provider]
        critical_issues = len([c for c in provider_checks if c.severity == SeverityLevel.CRITICAL and c.status == StatusLevel.FAILING])
        provider_stats[provider] = {
            "total": len(provider_checks),
            "critical": critical_issues
        }
    
    # Get recent violations (failing checks)
    recent_violations = failing_checks[:10]  # Latest 10 violations
    
    return DashboardSummary(
        total_checks=total_checks,
        compliant=compliant,
        non_compliant=non_compliant,
        critical_count=critical_count,
        framework_scores=framework_scores,
        provider_stats=provider_stats,
        recent_violations=recent_violations
    )

def get_mock_ai_insights() -> AiInsights:
    """Generate mock AI insights data"""
    checks = get_mock_compliance_checks()
    violations = [c for c in checks if c.status == StatusLevel.FAILING]
    critical_violations = [c for c in violations if c.severity == SeverityLevel.CRITICAL]
    
    frameworks_affected = len(set(v.framework for v in violations))
    
    summary = {
        "total_violations": len(violations),
        "critical_violations": len(critical_violations),
        "frameworks_affected": frameworks_affected,
        "last_updated": datetime.now().isoformat()
    }
    
    recommendations = [
        {
            "priority": "Critical",
            "description": "Implement end-to-end encryption for all data transmissions",
            "action": "Configure TLS 1.3 for all service communications and enable encryption at rest"
        },
        {
            "priority": "High",
            "description": "Update data retention policies to comply with GDPR requirements",
            "action": "Review and adjust data retention periods, implement automated data deletion"
        },
        {
            "priority": "High",
            "description": "Enhance healthcare data access logging and monitoring",
            "action": "Implement comprehensive audit logging for all healthcare data access and modifications"
        },
        {
            "priority": "Medium",
            "description": "Review and update business associate agreements",
            "action": "Conduct quarterly reviews of all BAAs and ensure compliance with current regulations"
        }
    ]
    
    return AiInsights(
        summary=summary,
        recommendations=recommendations
    )

