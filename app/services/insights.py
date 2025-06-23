from typing import List, Dict, Any
from app.ai_model import AIModel

_ai = AIModel  # instantiated in router

def generate_insights(violations: List[Dict[str, Any]]) -> Dict:
    return _ai.generate_insights(violations)