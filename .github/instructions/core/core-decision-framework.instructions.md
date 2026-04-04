# Core Decision Framework (UIA)

Pragmatic engineering standards to balance architectural excellence with delivery speed.

<rules>
- **WATCHGUARD:** If a project meets < 3 complexity criteria, prefer Simple Layered over Hexagonal.
- **KISS:** Always validate the simplest solution before proposing complexity.
- **DEBT:** Acknowledge technical debt explicitly when choosing speed over design.
- **AUTO-LINT:** Prefer automated tooling (Ruff, ESLint) over manual review.
</rules>

## The Watchguard Principle

Apply Hexagonal Architecture ONLY if at least 3 criteria are met:

1. Non-trivial business rules/domain logic to protect.
2. Multiple entry points planned (API, CLI, Queue).
3. Infrastructure is likely to change (e.g., swapping LLM providers).
4. codebase expected to grow significantly (>5000 lines).
5. Isolated domain testability is a hard requirement.

## Simple Layered Alternative

For small scripts or prototypes, use this structure instead:

- `models.py` (Data shapes)
- `services.py` (Logic)
- `repositories.py` (Data access)
- `api.py` (Entry point)

<success_criteria>

- No over-engineering of simple CRUD apps.
- Architecture choice is documented and justified.
- Technical debt is quantified and recorded.

</success_criteria>
