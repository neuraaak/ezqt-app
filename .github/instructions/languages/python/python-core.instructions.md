# Python Core Standards (UIA)

Core environment management, versioning, and foundational syntax for modern Python development.

<rules>
- **VERSION:** Target Python 3.11+ for native Performance and Syntax.
- **VENV:** Always use `.venv` for isolation; never install globally.
- **TOOLS:** ALWAYS use `uv` as the principal package manager, `mkdocs` for documentation, and `pre-commit` for quality gates.
- **RESOURCE:** Always use `with` statements (context managers) for resource cleanup.
- **SYNTAX:** Use `t-strings` (PEP 750) for safe templates where supported (3.14+).
</rules>

## Environment Management

- **ACTIVATE** `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix).
- **USE** `uv run` to execute tools and scripts inside the managed venv.
- **TEST** compatibility against multiple versions in CI/CD.

## Foundational Syntax (3.11+)

- **Union Types:** Use `int | str` instead of `Union[int, str]`.
- **Pathlib:** Use `pathlib.Path` exclusively for all filesystem operations.
- **Deferred Annotations:** Always use `from __future__ import annotations`.

<examples>
# 3.11+ Union and Pathlib usage
def get_file_size(path: str | Path) -> int:
    file_path = Path(path)
    with file_path.open("rb") as f:
        return len(f.read())
</examples>

<success_criteria>

- Virtual environment is active.
- Minimum Python 3.11 targeted.
- Resource management uses context managers.

</success_criteria>
