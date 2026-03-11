# AI Agent Instructions

This file contains instructions for all AI coding agents working on this project.

## Project Context

**Project Name**: {{my-project}}
**Tech Stack**: [Python 3.11+, ...]
**Environment**: [Corporate environment with proxy restrictions]

## Instruction Hierarchy

All project rules are centralized in `.github/instructions/`. The entry point is always the README, which is project-specific. The other files are generic and shared across projects.

| File                              | Role                                                                                               |
| --------------------------------- | -------------------------------------------------------------------------------------------------- |
| `.github/instructions/README.md`  | **Project-specific** — tech stack, architecture, conventions, overrides. **Read this first.**      |
| `.github/instructions/core/`      | Generic core principles (architecture, commits, cognitive conduct). Apply unless README overrides. |
| `.github/instructions/languages/` | Generic language standards (Python, JS). Apply unless README specifies otherwise.                  |

**Workflow**: Read `README.md` → identify relevant `core/` and `languages/` files → then code.

## Core Principles

1. **Always read project documentation first**
   - Start with `.github/instructions/README.md` — it is the authoritative source for this project
   - Consult relevant `core/` and `languages/` instruction files before coding

2. **Follow established patterns**
   - Review existing code before implementing new features
   - Maintain consistency with current architecture

3. **Security and compliance**
   - Never commit sensitive data (API keys, passwords, credentials)
   - Follow corporate security guidelines
   - Use environment variables for configuration

## Development Workflow

1. Read `.github/instructions/README.md` for project-specific context and overrides
2. Consult relevant instruction files from `.github/instructions/core/` and `.github/instructions/languages/`
3. Understand the task requirements completely
4. Plan the implementation approach
5. Write clean, well-documented code
6. Include tests where appropriate
7. Verify compliance with project standards

## File Organization

```text
project/
├── .github/
│   └── instructions/     # Project-specific rules and standards
├── src/                  # Source code
├── tests/                # Test files
└── docs/                 # Documentation
```

## Testing Requirements

- Write unit tests for new functionality
- Run existing tests before submitting changes
- Ensure code coverage meets project standards

## Documentation

- Add docstrings to all functions and classes
- Update README.md when adding new features
- Document any non-obvious implementation decisions

## Common Commands

```bash
# Run tests
pytest

# Lint code
mypy src/
ruff check src/

# Format code
black src/
```

## Important Notes

- Instructions in `.github/instructions/` override these general guidelines
- When in doubt, ask for clarification rather than making assumptions
- Prioritize code quality and maintainability over speed
