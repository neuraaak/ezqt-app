# Gemini-Specific Strategy (2026)

This profile leverages Gemini's (Google) massive context window and native multi-modal reasoning for complex codebase orchestration.

<rules>

- **BOOTSTRAP:** Always load the entire `.github/instructions/core/` directory to anchor reasoning.
- **MCP:** Adhere strictly to Model Context Protocol for type-safe tool interaction.
- **DURABILITY:** Implement Durable Checkpoints for long-running batch operations.

</rules>

## Long-Context Utilization

Gemini is optimized for multi-file analysis. Use this to:

1. **Cross-Check:** Validate changes against ALL relevant language UIAs in a single turn.
2. **Impact Analysis:** Before editing, use the large context to identify all potential side effects across the project.
3. **Pattern Recognition:** Use `core-hexagonal-architecture` to verify that no infrastructure leaks occur.

## Gemini Reasoning Protocols

- **Plan Mode:** Use for complex architectural refactoring.
- **Auto-Edit Mode:** For surgical fixes following `core-commits-git` standards.
- **Wait Policy:** If a task depends on multiple tool outputs, use `wait_for_previous=true`.

## 2026 Enterprise Stack

- **Package Manager:** Standardize on `uv` (Python) or `pnpm` (JS) as defined in language manifests.
- **Type Safety:** Prioritize `ty` (Python) or `TypeScript 6.0` (JS).
- **Security:** Follow `core-security-sanitization` for all I/O boundary logic.

<success_criteria>

- Large context used to prevent regressions.
- Tooling calls are parallelized for efficiency.
- Changes are atomized and fully documented.

</success_criteria>
