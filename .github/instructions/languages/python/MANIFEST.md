# Python Instructions Manifest

This manifest defines the modular structure of Python development standards. All modules are designed to be "Atomic Instruction Units" (UIA) for optimal context management in 2026 AI-driven development.

<rules>
- **AGENT DIRECTIVE:** Always consult the relevant submodule based on the task context.
- **PRECEDENCE:** These modules take precedence over general Python defaults.
- **VERSION:** Target Python 3.11+ minimum, with 3.14+ (GIL-less) optimizations where applicable.
</rules>

## Modules

| Module                                           | Description                  | Key Focus                                                       |
| :----------------------------------------------- | :--------------------------- | :-------------------------------------------------------------- |
| `python-core.instructions.md`                    | Core environment and syntax  | Venv, 3.11+ syntax, resource management.                        |
| `python-typing.instructions.md`                  | Advanced Type System         | Native generics, Protocols, TypedDict, Literal.                 |
| `python-style-layout.instructions.md`            | Visual & Documentation Style | Section markers, imports, Google docstrings.                    |
| `python-project-config.instructions.md`          | Project Configuration        | `pyproject.toml`, Ruff, dependencies, tool sync.                |
| `python-concurrency-performance.instructions.md` | Performance & Scale          | Asyncio, Free-Threaded Python, large datasets.                  |
| `python-testing-quality.instructions.md`         | Testing & Validation         | Pytest, coverage, property-based testing.                       |
| `python-security-ops.instructions.md`            | Security & Production        | Secrets, Docker, Observability, Tachyon.                        |
| `python-architecture-design.instructions.md`     | Architecture & Visibility    | `__all__`, design patterns, symbol visibility.                  |
| `python-docs.instructions.md`                    | Documentation Standards      | Diátaxis quadrants, MkDocs Material, mkdocstrings, admonitions. |

<success_criteria>

- No information overlap between modules.
- All files contain 2026 hybrid XML/Markdown tagging.
- Python 3.11+ as the baseline version.

</success_criteria>
