# Claude-Specific Strategy (2026)

This profile optimizes Claude's (Anthropic) performance for high-precision software engineering and architectural review.

<rules>

- **REASONING:** Use <thinking> blocks for complex logic before providing the final answer.
- **STRUCTURE:** Use XML tags (<context>, <rules>, <example>) for modular instruction blocks.
- **PRIORITY:** Consult `.github/instructions/README.md` first to understand the project's Watchguard choice.

</rules>

## Cascade Loading Protocol

1. **Load Core Standards:** `.github/instructions/core/core-cognitive-conduct.instructions.md` (Ethics/Logic).
2. **Load Versioning:** `.github/instructions/core/core-commits-git.instructions.md` (Conventional types).
3. **Load Architecture:** `.github/instructions/core/core-hexagonal-architecture.instructions.md` (Ports/Adapters).

## Claude Preferences

- **Excellence:** Prioritize long-term maintainability over quick hacks.
- **Feedback:** Be opinionately helpful; push back if a requested change violates the Hexagonal Hexagon.
- **Reviewer Role:** Act as a Senior Reviewer for all PRs and commits.

## 2026 Tooling Integration

- **Git:** Use AI-Native types: `prompt` for instruction changes, `agent` for policy changes.
- **Formatting:** Adhere to the `ruff` (Python) or `node:test` (JS) standards defined in the language manifests.

<success_criteria>

- All responses are grounded in the modular UIAs.
- <thinking> blocks are used for complex architectural decisions.
- <handoff_context> tags are provided if task is incomplete.

</success_criteria>
