from services.control_plane import execute


def main():
    capabilities = execute("capabilities")
    assert capabilities["tool"] == "capability_list"
    assert len(capabilities["capabilities"]) >= 4

    memory = execute("memory: What have I said about GitHub?")
    assert memory["tool"] == "personal_memory"
    assert "count" in memory

    blocked = execute("research: MCP architecture")
    assert blocked["tool"] == "web_research"
    assert "confirmation" in blocked["error"].lower()

    audit = execute("audit")
    assert audit["tool"] == "audit_log"
    assert len(audit["events"]) >= 1

    print("CONTROL PLANE TEST PASSED")


if __name__ == "__main__":
    main()
