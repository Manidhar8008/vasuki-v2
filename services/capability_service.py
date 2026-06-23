import json
from pathlib import Path

CAPABILITIES_FILE = Path(__file__).resolve().parent.parent / "config" / "capabilities.json"


def list_capabilities() -> dict:
    data = json.loads(CAPABILITIES_FILE.read_text(encoding="utf-8"))
    return {
        "tool": "capability_list",
        "version": data.get("version", "unknown"),
        "capabilities": data.get("capabilities", []),
    }


def get_capability(capability_id: str) -> dict | None:
    for item in list_capabilities()["capabilities"]:
        if item["id"] == capability_id:
            return item
    return None


def can_run(capability_id: str, confirmed: bool = False) -> dict:
    capability = get_capability(capability_id)

    if capability is None:
        return {"allowed": False, "reason": "Capability is not registered."}

    if capability.get("requires_confirmation", False) and not confirmed:
        return {
            "allowed": False,
            "reason": "Explicit confirmation is required before this capability can run.",
            "capability": capability,
        }

    return {"allowed": True, "capability": capability}
