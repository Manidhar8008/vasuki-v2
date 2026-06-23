import json
from pathlib import Path

CAPABILITIES_FILE = Path("config/capabilities.json")


def list_capabilities() -> dict:
    data = json.loads(CAPABILITIES_FILE.read_text(encoding="utf-8"))
    return {
        "tool": "capability_list",
        "version": data.get("version", "unknown"),
        "capabilities": data.get("capabilities", []),
    }


def get_capability(capability_id: str) -> dict | None:
    for capability in list_capabilities()["capabilities"]:
        if capability["id"] == capability_id:
            return capability
    return None


def can_run(capability_id: str, confirmed: bool = False) -> dict:
    capability = get_capability(capability_id)

    if not capability:
        return {
            "allowed": False,
            "reason": "Capability is not registered."
        }

    if capability.get("requires_confirmation") and not confirmed:
        return {
            "allowed": False,
            "reason": "This capability requires explicit confirmation.",
            "capability": capability
        }

    return {
        "allowed": True,
        "capability": capability
    }
