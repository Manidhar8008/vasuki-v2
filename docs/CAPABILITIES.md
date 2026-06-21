# VASUKI v2 — Capability Manifest

## Active capabilities

| Capability | Service | Status |
|---|---|---|
| Memory search | services/memory_service.py | Active |
| Project planning | services/planner_service.py | Active |
| Mentor guidance | services/mentor_service.py | Active |
| System health | services/status_service.py | Active |
| GitHub repository status | services/github_service.py | Active |
| Local file search | services/file_search_service.py | Active |
| Command routing | api/command_router.py | Active |
| Audit logging | services/audit_service.py | Active |

## Command flow

User query
→ Tool picker
→ Service registry
→ Selected tools
→ Audit log
→ Structured response

## Current boundary

Vasuki can inspect and organize local project information.
Vasuki does not autonomously modify, delete, upload, purchase, message, or control external systems.
