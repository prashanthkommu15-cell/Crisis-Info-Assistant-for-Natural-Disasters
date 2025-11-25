from typing import Dict
from project.core.a2a_protocol import make_plan_message
from project.memory.session_memory import default_memory

class Planner:
    def __init__(self, memory=default_memory):
        self.memory = memory

    def parse_intent(self, user_input: str) -> Dict:
        ui = user_input.lower()
        hazard = None
        if any(w in ui for w in ["flood","flooding","water level","inundation"]):
            hazard = "flood"
        elif any(w in ui for w in ["earthquake","quake","tremor"]):
            hazard = "earthquake"
        elif any(w in ui for w in ["wildfire","wildfires","bushfire"]):
            hazard = "wildfire"
        elif any(w in ui for w in ["storm","typhoon","hurricane","cyclone"]):
            hazard = "storm"
        else:
            hazard = "general"

        location = None
        if " in " in user_input:
            parts = user_input.split(" in ")
            location = parts[-1].strip().rstrip("?.!")
        elif " near " in user_input:
            parts = user_input.split(" near ")
            location = parts[-1].strip().rstrip("?.!")
        else:
            location = self.memory.get_long_term("preferred_region", None)

        return {"hazard": hazard, "location": location}

    def create_plan(self, user_input: str) -> Dict:
        intent = self.parse_intent(user_input)
        plan = make_plan_message(
            task_type="fetch_and_summarize",
            location=intent.get("location"),
            data_sources=["rss","newsapi","websearch"],
            language="en",
            detail_level="simple",
            hazard=intent.get("hazard")
        )
        return plan
