from services.memory_service import search_memory
from services.planner_service import create_plan
from services.mentor_service import mentor_response
from services.status_service import get_status

TOOLS = {
    "memory_search": search_memory,
    "project_planner": create_plan,
    "mentor": mentor_response,
    "system_status": lambda query=None: get_status(),
}

def get_tool(name: str):
    return TOOLS.get(name)

