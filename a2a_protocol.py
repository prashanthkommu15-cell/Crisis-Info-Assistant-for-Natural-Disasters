from typing import Dict, List, Optional
def make_plan_message(task_type: str, location: Optional[str] = None, data_sources: Optional[List[str]] = None, language: str = "en", detail_level: str = "simple", hazard: Optional[str] = None) -> Dict:
    return {
        "task_type": task_type,
        "location": location,
        "data_sources": data_sources or [],
        "language": language,
        "detail_level": detail_level,
        "hazard": hazard
    }
def make_worker_result(summary: str, safety: str, sources: Optional[List[str]] = None, confidence: float = 0.5) -> Dict:
    return {
        "crisis_summary": summary,
        "safety_instructions": safety,
        "sources": sources or [],
        "confidence": confidence
    }
