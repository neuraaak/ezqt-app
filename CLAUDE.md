# Claude-Specific Instructions

This file contains instructions specifically for Claude (Anthropic) when working on this project.

## Project Overview

This project follows a structured approach with centralized instructions in `.github/instructions/`.

**CRITICAL**: Before any development task, consult `.github/instructions/README.md` and relevant domain-specific files.

## Instruction Hierarchy

1. `.github/instructions/README.md` - Project context and overrides
2. `.github/instructions/core/` - Core principles and architecture
3. `.github/instructions/languages/python/` - Python-specific standards
4. This file (CLAUDE.md) - Claude-specific preferences

## Code Generation Preferences

### Python Development

- Use type hints consistently (follow `.github/instructions/languages/python/python-development-standards.instructions.md`)
- Prefer `pathlib` over `os.path`
- Use f-strings for string formatting
- Follow PEP 8 conventions
- Add comprehensive docstrings (Google style)

### Error Handling

```python
# Preferred pattern
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### Testing Approach

- Write tests using pytest
- Use descriptive test names: `test_should_<expected_behavior>_when_<condition>`
- Include both happy path and edge cases

## Communication Style

- Explain architectural decisions concisely
- Highlight potential issues or trade-offs
- Ask clarifying questions when requirements are ambiguous
- Suggest improvements when you notice technical debt

## Corporate Environment Constraints

- Proxy configuration required for external requests
- Use wheel files for dependencies (`.whl`)
- Limited access to PyPI - assume local package management
- Windows-based development environment

## Tool Preferences

- **Type Checking**: mypy (configured in project)
- **Formatting**: black, ruff
- **Build**: cx_Freeze for executables
- **Version Control**: Git with conventional commits

## Prohibited Practices

- Never use `print()` for logging (use `logging` module)
- Avoid global variables
- Don't commit commented-out code
- No hard-coded credentials or file paths

## Before Starting Any Task

1. Run `view .github/instructions/` to check available guidance
2. Read relevant instruction files for the task type
3. Review existing similar code for patterns
4. Verify understanding of requirements
5. Propose approach if task is complex

## Response Format Preferences

- Start with a brief summary of the approach
- Provide complete, runnable code
- Include import statements
- Add inline comments for complex logic
- Suggest next steps or potential improvements

## File Modification Strategy

- Make minimal, focused changes
- Preserve existing code style
- Update related tests when modifying functionality
- Keep backwards compatibility unless explicitly asked to break it
