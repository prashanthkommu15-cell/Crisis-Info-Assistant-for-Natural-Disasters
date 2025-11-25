from typing import Dict
from project.core.observability import Logger

class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, worker_result: Dict) -> Dict:
        Logger.log({'agent':'evaluator','event':'evaluate_start','worker_result_summary': worker_result.get('crisis_summary','')[:200]})
        issues = []
        summary = (worker_result.get('crisis_summary') or '').strip()
        safety = (worker_result.get('safety_instructions') or '').strip()

        if not summary:
            issues.append('empty_summary')
        if not safety:
            issues.append('missing_safety_instructions')

        alarm_words = ['panic','apocalypse','catastrophic','devastating']
        lower = (summary + ' ' + safety).lower()
        for w in alarm_words:
            if w in lower:
                issues.append(f'alarm_word_{w}')

        final_confidence = worker_result.get('confidence',0.5)
        if issues:
            final_confidence = max(0.1, final_confidence - 0.3)

        approved = len(issues) == 0
        final_text = f"Summary:\n{summary}\n\nSafety Instructions:\n{safety}\n\nSources:\n" + ("\n".join(worker_result.get('sources',[])) or 'None')

        result = {
            'final_text': final_text,
            'confidence': final_confidence,
            'issues': issues,
            'approved': approved
        }
        Logger.log({'agent':'evaluator','event':'evaluate_complete','approved': approved, 'issues': issues, 'final_confidence': final_confidence})
        return result
