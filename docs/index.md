# EzQt-App

[![PyPI version](https://img.shields.io/pypi/v/ezqt-app?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/ezqt-app/)
[![Python versions](https://img.shields.io/pypi/pyversions/ezqt-app?style=flat&logo=python&logoColor=white)](https://pypi.org/project/ezqt-app/)
[![PyPI status](https://img.shields.io/pypi/status/ezqt-app?style=flat&logo=pypi&logoColor=white)](https://pypi.org/project/ezqt-app/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat&logo=github&logoColor=white)](https://github.com/neuraaak/ezqt-app/blob/main/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/neuraaak/ezqt-app/publish-pypi.yml?style=flat&label=publish&logo=githubactions&logoColor=white)](https://github.com/neuraaak/ezqt-app/actions/workflows/publish-pypi.yml)
[![Docs](https://img.shields.io/badge/docs-Github%20Pages-blue?style=flat&logo=materialformkdocs&logoColor=white)](https://neuraaak.github.io/ezqt-app/)
[![uv](https://img.shields.io/badge/package%20manager-uv-DE5FE9?style=flat&logo=uv&logoColor=white)](https://github.com/astral-sh/uv)
[![linter](https://img.shields.io/badge/linter-ruff-orange?style=flat&logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![type checker](https://img.shields.io/badge/type%20checker-ty-orange?style=flat&logo=astral&logoColor=white)](https://github.com/astral-sh/ty)

![EzQt-App logo](https://raw.githubusercontent.com/neuraaak/ezqt-app/refs/heads/main/docs/assets/logo-min.png)

**EzQt-App** is a PySide6 framework to bootstrap and structure desktop applications with a ready-to-use shell, configuration workflow, translation support, and reusable UI components.

## 🚀 Quick start

=== "uv"

    ```bash
    uv add ezqt-app
    ```

=== "pip"

    ```bash
    pip install ezqt-app
    ```

=== "From source"

    ```bash
    git clone https://github.com/neuraaak/ezqt-app.git
    cd ezqt_app && pip install .
    ```

Minimal application:

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App()
window.show()
sys.exit(app.exec())
```

## ✨ Key features

- **Application bootstrap**: `init`, assets generation, and project setup workflows
- **Modular services**: config, settings, runtime, translation, and UI service layers
- **Hexagonal architecture**: `domain` contracts with `services` adapters and explicit boundaries
- **Translation stack**: `.ts` loading + on-the-fly `.qm` compilation, `EzTranslator` Qt interceptor, non-blocking auto-translation with in-app progress indicator
- **Built-in CLI**: `ezqt` commands for init, tests, docs, and utility workflows
- **Test scopes**: unit, integration, and robustness test suites

## 📚 Documentation

| Section                                                                 | Description                                          |
| :---------------------------------------------------------------------- | :--------------------------------------------------- |
| [Getting Started](https://neuraaak.github.io/ezqt-app/getting-started/) | Installation, bootstrap, and first app               |
| [User Guides](https://neuraaak.github.io/ezqt-app/guides/)              | Development, testing, and styling guidance           |
| [API Reference](https://neuraaak.github.io/ezqt-app/api/)               | Service- and architecture-oriented API documentation |
| [CLI Reference](https://neuraaak.github.io/ezqt-app/cli/)               | Command-line utilities and command options           |
| [Examples](https://neuraaak.github.io/ezqt-app/examples/)               | Practical usage snippets for common scenarios        |
| [Concepts](https://neuraaak.github.io/ezqt-app/concepts/)               | Architecture rationale and design decisions          |

## 🎯 Main components

EzQt-App is organized around architectural modules:

### Domain module

- **`domain/ports`** — service contracts (protocols)
- **`domain/models`** — typed domain models and constants
- **`domain/results`** — typed initialization/result payloads

### Services module

- **`services/bootstrap`** — initialization sequence and options
- **`services/config`** — configuration load/save/path resolution
- **`services/settings`** — mutable app/gui settings state
- **`services/translation`** — language manager, helpers, auto-translation
- **`services/ui`** — UI orchestration services (theme/menu/panel/window)

### Widgets module

- **`widgets/core`** — application containers (`EzApplication`, `SettingsPanel`, etc.)
- **`widgets/extended`** — extended reusable controls

For detailed documentation, see [API Reference](https://neuraaak.github.io/ezqt-app/api/).

## 🧪 Testing

| Metric      | Value                         |
| :---------- | :---------------------------- |
| Test types  | Unit, Integration, Robustness |
| Runner      | `tests/run_tests.py`          |
| Output mode | Real-time streamed output     |

```bash
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type robustness
```

See the [Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/) for complete details.

## 📋 Requirements

- **Python** >= 3.11
- **PySide6** >= 6.7.3
- **PyYAML / ruamel.yaml** — configuration management

## ⚖️ License

MIT License — see [LICENSE](https://github.com/neuraaak/ezqt-app/blob/main/LICENSE) for details.
