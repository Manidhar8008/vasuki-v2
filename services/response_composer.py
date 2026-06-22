def compose_response(route_result: dict) -> str:
    query = route_result.get("query", "")
    results = route_result.get("results", [])

    lines = [f"VASUKI RESPONSE", f"Request: {query}", ""]

    if not results:
        return "\n".join(lines + ["No service produced a result."])

    for result in results:
        tool = result.get("tool", "unknown_tool")

        if "error" in result:
            lines.append(f"[{tool}] Error: {result['error']}")
            continue

        if tool == "system_status":
            lines.append("System status: healthy")
            lines.append(f"Database: {result.get('database', 'unknown')}")
            lines.append(f"Event log entries: {result.get('event_count', 0)}")
            tables = result.get("tables", [])
            lines.append(f"Tables: {', '.join(tables) if tables else 'none'}")

        elif tool == "github_status":
            lines.append("GitHub repository status")
            lines.append(f"Branch: {result.get('branch', 'unknown')}")
            lines.append(f"Repository: {result.get('remote', 'not configured')}")
            lines.append(f"Latest commit: {result.get('latest_commit', 'unknown')}")
            lines.append(
                "Working tree: clean"
                if result.get("clean")
                else "Working tree: changes detected"
            )

        elif tool == "memory_search":
            count = result.get("count", 0)
            lines.append(f"Memory search: {count} matching item(s)")
            for item in result.get("results", []):
                lines.append(f"- {item.get('value', '')}")

        elif tool == "project_planner":
            lines.append(f"Project plan: {result.get('goal', query)}")
            for phase in result.get("phases", []):
                lines.append(f"Phase {phase.get('phase')}: {phase.get('name')}")
                for task in phase.get("tasks", []):
                    lines.append(f"- {task}")
            lines.append(f"Next action: {result.get('next_action', '')}")

        elif tool == "mentor":
            lines.append("Mentor guidance")
            for step in result.get("method", []):
                lines.append(f"- {step}")
            lines.append(result.get("next_question", ""))

        else:
            lines.append(f"[{tool}] Result received.")

        lines.append("")

    return "\n".join(lines).strip()
