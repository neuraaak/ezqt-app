# Development guide

Complete guide for setting up the development environment and contributing to **ezqt_app**.

## 🔧 Prerequisites

- **Python** 3.11 or higher
- **PySide6** 6.x
- **Git** for version control

## 📝 Setup

Install the package in editable mode with all development dependencies:

=== "uv"

    ```bash
    git clone https://github.com/neuraaak/ezqt-app.git
    cd ezqt_app
    uv sync
    ```

=== "pip"

    ```bash
    git clone https://github.com/neuraaak/ezqt-app.git
    cd ezqt_app
    pip install -e ".[dev]"
    ```

Install pre-commit hooks:

=== "uv"

    ```bash
    uv add pre-commit
    pre-commit install
    ```

=== "pip"

    ```bash
    pip install pre-commit
    pre-commit install
    ```

## ⚙️ Development tools

### Formatting and linting

=== "Ruff"

    ```bash
    ruff format src tests
    ruff check src tests
    ```

=== "Type checking"

    ```bash
    # pyright is configured in pyproject.toml
    pyright src

    # ty (Astral type checker)
    ty check src
    ```

### Running tests

=== "By scope"

    ```bash
    python tests/run_tests.py --type unit
    python tests/run_tests.py --type integration
    python tests/run_tests.py --type robustness
    python tests/run_tests.py --type all
    ```

=== "With coverage"

    ```bash
    python tests/run_tests.py --coverage
    ```

=== "pytest directly"

    ```bash
    pytest tests/unit/ -v
    pytest tests/integration/ -v
    ```

## 📋 Code standards

- Formatting and linting: Ruff
- Type hints required on all public API symbols
- Google-style docstrings for all public functions and classes
- Section markers used consistently across project modules:

```python
# ///////////////////////////////////////////////////////////////
# SECTION NAME
# ///////////////////////////////////////////////////////////////
```

## 🔁 Pre-commit hooks

Pre-commit runs automatically on `git commit` and checks:

- Formatting and linting (Ruff)
- Import organization
- File hygiene (trailing whitespace, end-of-file newline, etc.)

To run manually against all files:

```bash
pre-commit run --all-files
```

## 🏗️ Architecture notes

The codebase follows a hexagonal migration approach:

| Layer    | Path        | Role                                    |
| :------- | :---------- | :-------------------------------------- |
| Domain   | `domain/`   | Contracts (protocols) and domain models |
| Services | `services/` | Adapters and orchestration              |
| Widgets  | `widgets/`  | Presentation layer                      |
| Kernel   | `kernel/`   | Legacy/infra layer (being reduced)      |

Bootstrap entry points:

- Python API: `ezqt_app.main.init(...)`
- CLI: `ezqt init`

See `src/ezqt_app/services/bootstrap/` for the initialization sequence.

## 📁 Project structure

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

## 🔁 Recommended workflow

### Before starting

=== "uv"

    ```bash
    uv sync
    pre-commit install
    ```

=== "pip"

    ```bash
    pip install -e ".[dev]"
    pre-commit install
    ```

### During development

```bash
ruff format src tests
ruff check src tests
pytest tests/unit/ -v
```

### Before pushing

```bash
python tests/run_tests.py --type all
python tests/run_tests.py --coverage
```

## 💻 Built-in CLI

The project exposes a CLI via `ezqt`:

```bash
ezqt info
ezqt init --verbose
ezqt docs --serve
```

See [CLI Reference](../cli/index.md) for the full command reference.

## Troubleshooting

| Issue                 | Solution                                                 |
| :-------------------- | :------------------------------------------------------- |
| CLI command not found | Reinstall editable package: `pip install -e ".[dev]"`    |
| Qt import errors      | Verify PySide6 environment: `python -c "import PySide6"` |
| Missing config files  | Run `ezqt init` in project root                          |

## ➡️ Related

- [Testing guide](testing.md) — test suite scopes and fixtures
- [API reference](../api/index.md) — complete service documentation
- [CLI reference](../cli/index.md) — command-line interface
- [QSS style guide](style-guide.md) — visual customization
