from api.command_router import route_command

def ask(query: str) -> dict:
    return route_command(query)
