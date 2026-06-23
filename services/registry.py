from services.memory_service import search_memory
from services.planner_service import create_plan
from services.mentor_service import mentor_response
from services.status_service import get_status
from services.github_service import get_github_status
from services.reasoning_service import general_reasoning


TOOLS = {
    "memory_search": search_memory,
    "project_planner": create_plan,
    "mentor": mentor_response,
    "system_status": lambda query=None: get_status(),
    "github_status": lambda query=None: get_github_status(),
    "general_reasoning": general_reasoning,
}


def get_tool(name: str):
    return TOOLS.get(name)
