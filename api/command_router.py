from services.tool_picker import pick_tools
from services.registry import get_tool
from services.audit_service import log_action

def route_command(query: str) -> dict:
    selected_tools = pick_tools(query)
    outputs = []

    for tool_name in selected_tools:
        tool = get_tool(tool_name)

        if tool is None:
            outputs.append({
                "tool": tool_name,
                "error": "Tool is not registered yet",
            })
            continue

        try:
            result = tool(query)
            outputs.append(result)
            log_action("command_router", tool_name, query)
        except Exception as error:
            outputs.append({
                "tool": tool_name,
                "error": str(error),
            })

    return {
        "query": query,
        "selected_tools": selected_tools,
        "results": outputs,
    }
