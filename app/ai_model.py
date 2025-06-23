import joblib
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException
import warnings

class AIModel:
    def __init__(self, model_path: str):
        self.model = None
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Warning: Failed to load model from {model_path}: {e}")
            print("AI model will use fallback implementation")
            self.model = None

    def generate_insights(self, violations: List[Dict[str, Any]]) -> Dict:
        # Guarantee structured output even if no violations
        if not violations:
            return {
                "summary": {
                    "total_violations": 0,
                    "critical_violations": 0,
                    "frameworks_affected": 0,
                    "last_updated": datetime.utcnow().isoformat()
                },
                "recommendations": []
            }

        try:
            # If model is not available, use fallback logic
            if self.model is None:
                return self._fallback_insights(violations)

            # Feature‐engineering
            X = np.array([
                [
                    1 if v["severity"] == "Critical" else 0,
                    1 if v["severity"] == "High" else 0,
                    v["risk_score"],
                    len(v["description"])
                ] for v in violations
            ])

            # Your model's API:
            priorities   = self.model.predict_priority(X)
            descriptions = self.model.predict_description(X)
            actions      = self.model.predict_action(X)

            recs = [
                {"priority": p, "description": d, "action": a}
                for p, d, a in zip(priorities, descriptions, actions)
            ]

            return {
                "summary": {
                    "total_violations": len(violations),
                    "critical_violations": sum(v["severity"] == "Critical" for v in violations),
                    "frameworks_affected": len({v["framework"] for v in violations}),
                    "last_updated": datetime.utcnow().isoformat()
                },
                "recommendations": recs
            }

        except Exception as e:
            print(f"AI inference failed: {e}, using fallback")
            return self._fallback_insights(violations)

    def _fallback_insights(self, violations: List[Dict[str, Any]]) -> Dict:
        """Fallback implementation when model is not available"""
        critical_violations = [v for v in violations if v["severity"] == "Critical"]
        high_violations = [v for v in violations if v["severity"] == "High"]
        
        recommendations = []
        
        if critical_violations:
            recommendations.append({
                "priority": "High",
                "description": f"Address {len(critical_violations)} critical violations immediately",
                "action": "Review and fix critical compliance issues"
            })
        
        if high_violations:
            recommendations.append({
                "priority": "Medium", 
                "description": f"Address {len(high_violations)} high-severity violations",
                "action": "Schedule remediation for high-priority issues"
            })
        
        if len(violations) > len(critical_violations) + len(high_violations):
            recommendations.append({
                "priority": "Low",
                "description": "Review remaining compliance violations",
                "action": "Plan systematic review of all violations"
            })

        return {
            "summary": {
                "total_violations": len(violations),
                "critical_violations": len(critical_violations),
                "frameworks_affected": len({v["framework"] for v in violations}),
                "last_updated": datetime.utcnow().isoformat()
            },
            "recommendations": recommendations
        }