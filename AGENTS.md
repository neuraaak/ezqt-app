# AI Agent Instructions

This file contains instructions for all AI coding agents working on this project.

## Project Context

**Project Name**: [Your Project Name]
**Tech Stack**: Python 3.11+, FastAPI, PostgreSQL
**Environment**: Corporate environment with proxy restrictions

## Core Principles

1. **Always read project documentation first**
   - Check `.github/instructions/README.md` for project-specific context
   - Consult relevant files in `.github/instructions/` before coding

2. **Follow established patterns**
   - Review existing code before implementing new features
   - Maintain consistency with current architecture

3. **Security and compliance**
   - Never commit sensitive data (API keys, passwords, credentials)
   - Follow corporate security guidelines
   - Use environment variables for configuration

## Development Workflow

1. Read relevant instruction files from `.github/instructions/`
2. Understand the task requirements completely
3. Plan the implementation approach
4. Write clean, well-documented code
5. Include tests where appropriate
6. Verify compliance with project standards

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
