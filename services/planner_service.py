def create_plan(goal: str) -> dict:
    return {
        "tool": "project_planner",
        "goal": goal,
        "phases": [
            {
                "phase": 1,
                "name": "Define",
                "tasks": [
                    "Clarify the expected outcome",
                    "List constraints and available resources",
                    "Define a measurable success condition"
                ]
            },
            {
                "phase": 2,
                "name": "Build",
                "tasks": [
                    "Break work into small deliverables",
                    "Implement the highest-priority deliverable",
                    "Record each completed action"
                ]
            },
            {
                "phase": 3,
                "name": "Validate",
                "tasks": [
                    "Run tests",
                    "Check output against success condition",
                    "Log lessons and next improvements"
                ]
            }
        ],
        "next_action": "Write the smallest concrete task that can be completed now."
    }
