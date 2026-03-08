# Development Guide

Complete guide for setting up development workflow and contributing to **ezqt_app**.

---

## Prerequisites

- **Python**: 3.10 or higher
- **PySide6**: 6.x
- **Git**: for version control

---

## Setup

```bash
pip install -e ".[dev]"

# Or with Make
make install-dev
```

---

## Development Tools

### Code Formatting

- Ruff for formatting and linting
- Type checking with `pyright` and `ty`

### Development Commands

```bash
ruff format src tests
ruff check src tests
pytest
```

Project test runner shortcuts:

```bash
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type robustness
python tests/run_tests.py --coverage
```

---

## Quality Tooling

```bash
ruff check src tests
ruff format src tests
pytest
```

Type checks configured in `pyproject.toml`:

- `pyright`
- `ty`

---

## Code Standards

- formatting/linting with Ruff
- type hints required on public API
- Google-style docstrings
- section markers used across project modules

### Section Markers

```python
# ///////////////////////////////////////////////////////////////
# SECTION NAME
# ///////////////////////////////////////////////////////////////
```

---

## Pre-commit Hooks

### Installation

```bash
pip install pre-commit
pre-commit install
```

### Automatic Checks

- formatting and linting
- import organization
- file hygiene checks

## Architecture Notes

Current codebase follows a hexagonal migration approach:

- `domain/`: contracts and domain models
- `services/`: adapters and orchestration
- `widgets/`: presentation layer
- `kernel/`: legacy/infra layer being reduced

---

## Bootstrap Entry Points

- Python API: `ezqt_app.main.init(...)`
- CLI: `ezqt init`

See `src/ezqt_app/services/bootstrap/` for initialization sequence.

---

## Tests

### Test Structure

```text
tests/
├── conftest.py
├── run_tests.py
├── unit/
├── integration/
└── robustness/
```

### Running Tests

```bash
python tests/run_tests.py --type all
python tests/run_tests.py --coverage
```

---

## Built-in CLI

The project exposes a CLI via `ezqt`:

```bash
ezqt info
ezqt init --verbose
ezqt test --unit --coverage
ezqt docs --serve
```

---

## Recommended Workflow

### 1. Before Starting

```bash
pip install -e ".[dev]"
```

### 2. During Development

```bash
ruff format src tests
ruff check src tests
pytest
```

### 3. Before Pushing

```bash
python tests/run_tests.py --type all
python tests/run_tests.py --coverage
```

---

## Project Structure

```text
src/ezqt_app/
├── domain/
├── services/
├── widgets/
├── utils/
└── cli/

tests/
docs/
```

---

## Troubleshooting

| Issue                 | Solution                        |
| --------------------- | ------------------------------- |
| CLI command not found | Reinstall editable package      |
| Qt import errors      | Verify PySide6 environment      |
| Missing config files  | Run `ezqt init` in project root |

---

## Resources

- [API Reference](https://neuraaak.github.io/ezqt-app/api/) -- Complete widget documentation
- [Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/) -- Testing guidelines and best practices
- [QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/) -- Visual customization
- [CLI Reference](https://neuraaak.github.io/ezqt-app/cli/) -- Command-line interface
