# Welcome to EzQt App Documentation

[![PyPI](https://img.shields.io/badge/PyPI-ezqt--app-orange.svg)](https://pypi.org/project/ezqt-app/)
[![PyPI version](https://img.shields.io/pypi/v/ezqt-app)](https://pypi.org/project/ezqt-app/)
[![Python versions](https://img.shields.io/pypi/pyversions/ezqt-app)](https://pypi.org/project/ezqt-app/)
[![License](https://img.shields.io/pypi/l/ezqt-app)](https://github.com/neuraaak/ezqt-app/blob/main/LICENSE)

**EzQt App** is a PySide6 framework to bootstrap and structure desktop applications with a ready-to-use shell, configuration workflow, translation support, and reusable UI components.

## ✨ Key Features

- **✅ Application Bootstrap**: `init`, assets generation, and project setup workflows
- **✅ Modular Services**: config, settings, runtime, translation, and UI service layers
- **✅ Hexagonal Migration**: `domain` contracts with `services` adapters and explicit boundaries
- **✅ Translation Stack**: `.ts` loading + on-the-fly `.qm` compilation, `EzTranslator` Qt interceptor, non-blocking auto-translation with in-app progress indicator
- **✅ Built-in CLI**: `ezqt` commands for init, tests, docs, and utility workflows
- **✅ Test Scopes**: unit, integration, and robustness test suites

## 🚀 Quick Start

### Installation

```bash
pip install ezqt-app
```

Or from source:

```bash
git clone https://github.com/neuraaak/ezqt-app.git
cd ezqt_app && pip install .
```

### First App

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App()
window.show()
sys.exit(app.exec())
```

## 📚 Documentation Structure

| Section                                                                 | Description                                          |
| ----------------------------------------------------------------------- | ---------------------------------------------------- |
| [Getting Started](https://neuraaak.github.io/ezqt-app/getting-started/) | Installation, bootstrap, and first app               |
| [API Reference](https://neuraaak.github.io/ezqt-app/api/)               | Service- and architecture-oriented API documentation |
| [User Guides](https://neuraaak.github.io/ezqt-app/guides/)              | Development, testing, and styling guidance           |
| [Examples](https://neuraaak.github.io/ezqt-app/examples/)               | Practical usage snippets for common scenarios        |
| [CLI Reference](https://neuraaak.github.io/ezqt-app/cli/)               | Command-line utilities and command options           |

## 🎯 Main Components

EzQt App is organized around architectural modules:

### Domain Module

- **`domain/ports`** - Service contracts (protocols)
- **`domain/models`** - Typed domain models and constants
- **`domain/results`** - Typed initialization/result payloads

### Services Module

- **`services/bootstrap`** - Initialization sequence and options
- **`services/config`** - Configuration load/save/path resolution
- **`services/settings`** - Mutable app/gui settings state
- **`services/translation`** - Language manager, helpers, auto-translation
- **`services/ui`** - UI orchestration services (theme/menu/panel/window)

### Widgets Module

- **`widgets/core`** - Application containers (`EzApplication`, `SettingsPanel`, etc.)
- **`widgets/extended`** - Extended reusable controls

For detailed documentation, see [API Reference](https://neuraaak.github.io/ezqt-app/api/).

## 🧪 Testing

Current suite is split into dedicated scopes:

| Metric      | Value                         |
| ----------- | ----------------------------- |
| Test types  | Unit, Integration, Robustness |
| Runner      | `tests/run_tests.py`          |
| Output mode | Real-time streamed output     |

Run tests with:

```bash
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type robustness
```

See the [Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/) for complete details.

## 📦 Core Dependencies

- **PySide6 >= 6.7.3** - Qt for Python runtime
- **Python >= 3.10** - Language/runtime target
- **PyYAML / ruamel.yaml** - Configuration management

## 📝 License

MIT License – See [LICENSE](https://github.com/neuraaak/ezqt-app/blob/main/LICENSE) file for details.

## 🔗 Links

- **Repository**: [https://github.com/neuraaak/ezqt-app](https://github.com/neuraaak/ezqt-app)
- **PyPI**: [https://pypi.org/project/ezqt-app/](https://pypi.org/project/ezqt-app/)
- **Issues**: [https://github.com/neuraaak/ezqt-app/issues](https://github.com/neuraaak/ezqt-app/issues)
- **Documentation**: [https://neuraaak.github.io/ezqt-app/](https://neuraaak.github.io/ezqt-app/)

---

**EzQt App** - Structured, practical PySide6 app framework with a complete bootstrap workflow.
