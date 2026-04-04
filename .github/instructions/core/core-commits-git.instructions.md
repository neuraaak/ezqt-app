# Core Commits & Git Standards (UIA)

Professional commit framework for clean, traceable, and AI-navigable project history.

<rules>
- **ATOMIC:** One purpose per commit (feat, fix, refactor, prompt, agent).
- **TYPES:** Use Conventional Commits. NEW for 2026: `prompt` and `agent`.
- **STYLE:** Imperative mood; max 50 chars for subject; body explains "WHY", not "WHAT".
- **HYGIENE:** Never commit secrets, generated files, or "WIP" noise on shared branches.
</rules>

## Standard Type Prefixes

| Type            | Description                                                            |
| :-------------- | :--------------------------------------------------------------------- |
| `feat` / `fix`  | New functionality or bug correction.                                   |
| `prompt`        | Changes to LLM instructions, system prompts, or .md instruction files. |
| `agent`         | Changes to agentic policies, tool definitions, or MCP configurations.  |
| `refactor`      | Code restructuring without behavior change.                            |
| `docs` / `test` | Documentation or test updates only.                                    |

## Staging Discipline

- **REVIEW** every diff before staging.
- **STAGE BY NAME:** Prefer explicit file paths over `git add .`.
- **SECURE:** Inspect for debug code, console.log, or credentials before committing.

<examples>
# Standard Commit Message
feat(auth): implement OIDC provider using hexagonal adapters

The legacy JWT provider lacked session invalidation. Moving to OIDC
enables centralized identity management and better audit trails.

# AI-Native Commit Message

prompt(python): modularize instructions into UIA submodules

Splitting monolithic files into atomized units improves agent
attention and reduces context window pressure.
</examples>

<success_criteria>

- Commit history tells a coherent story.
- Types accurately reflect the change.
- No secrets or WIP commits in project history.

</success_criteria>
