def pick_tools(query: str) -> list[str]:
    q = query.lower()
    tools = []

    if any(word in q for word in ["memory", "remember", "history", "past", "context"]):
        tools.append("memory_search")

    if any(word in q for word in ["plan", "project", "roadmap", "goal", "task"]):
        tools.append("project_planner")

    if any(word in q for word in ["status", "health", "check", "alive"]):
        tools.append("system_status")

    if any(word in q for word in ["learn", "mentor", "career", "improve", "study"]):
        tools.append("mentor")

    if any(word in q for word in ["search", "find", "file", "document"]):
        tools.append("local_search")

    if any(word in q for word in ["github", "git", "commit", "branch", "repository", "repo"]):
        tools.append("github_status")

    return tools or ["general_reasoning"]
