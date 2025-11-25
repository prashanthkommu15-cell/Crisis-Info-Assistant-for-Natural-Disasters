from typing import Dict
from project.agents.planner import Planner
from project.agents.worker import Worker
from project.agents.evaluator import Evaluator
from project.memory.session_memory import default_memory
from project.core.observability import Logger

class MainAgent:
    def __init__(self):
        self.memory = default_memory
        self.planner = Planner(memory=self.memory)
        self.worker = Worker(memory=self.memory)
        self.evaluator = Evaluator()

    def handle_message(self, user_input: str) -> Dict:
        Logger.log({'agent': 'main', 'event': 'handle_message_received', 'input': user_input})
        plan = self.planner.create_plan(user_input)
        Logger.log({'agent': 'planner', 'plan': plan})

        worker_result = self.worker.execute(plan)
        Logger.log({'agent': 'worker', 'worker_result': {'summary': worker_result.get('crisis_summary', '')[:200], 'confidence': worker_result.get('confidence')}})

        final = self.evaluator.evaluate(worker_result)
        Logger.log({'agent': 'evaluator', 'final': {'approved': final.get('approved'), 'confidence': final.get('confidence')}})

        response = {
            'response': final.get('final_text'),
            'confidence': final.get('confidence'),
            'approved': final.get('approved'),
            'issues': final.get('issues')
        }
        return response

def run_agent(user_input: str):
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result['response']
