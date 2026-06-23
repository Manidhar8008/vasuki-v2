from services.capability_service import can_run, list_capabilities
from services.audit_service import record_tool_event, recent_audit
from services.memory_answer_service import answer_from_memory

try:
    from services.github_service import get_github_status
except ImportError:
    get_github_status = None


def execute(command: str, confirmed: bool = False) -> dict:
    raw = command.strip()
    normalized = raw.lower()

    if normalized in {"capabilities", "plugins", "tools"}:
        result = list_capabilities()
        record_tool_event("capability_list", raw, True, "listed capabilities")
        return result

    if normalized in {"audit", "audit log", "history"}:
        result = recent_audit()
        record_tool_event("audit_log", raw, True, "read audit log")
        return result

    if normalized.startswith("memory:"):
        query = raw.split(":", 1)[1].strip()
        permission = can_run("personal_memory", confirmed)

        if not permission["allowed"]:
            record_tool_event("personal_memory", raw, False, permission["reason"])
            return {"tool": "personal_memory", "error": permission["reason"]}

        result = answer_from_memory(query)
        record_tool_event("personal_memory", raw, True, f"returned {result.get('count', 0)} evidence items")
        return result

    if normalized in {"github status", "github"}:
        permission = can_run("github_status", confirmed)

        if not permission["allowed"]:
            record_tool_event("github_status", raw, False, permission["reason"])
            return {"tool": "github_status", "error": permission["reason"]}

        if get_github_status is None:
            outcome = "GitHub connector is unavailable."
            record_tool_event("github_status", raw, False, outcome)
            return {"tool": "github_status", "error": outcome}

        result = get_github_status()
        record_tool_event("github_status", raw, True, "read repository status")
        return result

    if normalized.startswith("research:"):
        permission = can_run("web_research", confirmed)
        outcome = permission.get("reason", "Web research connector is not implemented yet.")
        record_tool_event("web_research", raw, permission["allowed"], outcome)

        if not permission["allowed"]:
            return {
                "tool": "web_research",
                "error": outcome,
                "next_step": "Re-run with confirmed=True only after reviewing the request."
            }

        return {
            "tool": "web_research",
            "error": "Connector placeholder: public-web research is not implemented yet."
        }

    return {
        "tool": "control_plane",
        "error": (
            "Unknown command. Use: capabilities | memory: <question> | "
            "github status | audit | research: <topic>"
        ),
    }
