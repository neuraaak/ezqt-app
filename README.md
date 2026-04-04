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

![Logo](docs/assets/logo-min.png)

**EzQt-App** is a PySide6 framework to bootstrap and structure desktop applications with a ready-to-use shell, configuration workflow, translation support, and reusable UI components.

## 🚀 Quick start

Install with uv:

```bash
uv add ezqt-app
```

Install with pip:

```bash
pip install ezqt-app
```

From source:

```bash
git clone https://github.com/neuraaak/ezqt-app.git
cd ezqt_app
pip install .
```

Minimal application:

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App().build()
window.show()
sys.exit(app.exec())
```

## ✨ Key features

- Application bootstrap: init, assets generation, and project setup workflows
- Modular services: config, settings, runtime, translation, and UI orchestration
- Hexagonal architecture: domain contracts, service adapters, and clean boundaries
- Translation stack: .ts loading + .qm lifecycle, EzTranslator interceptor, non-blocking auto-translation
- Built-in CLI: commands for project init/create, docs, info, and translation conversion
- Typed codebase: Python 3.11+ with strict linting/typing toolchain

## 📚 Documentation

- [Getting Started](https://neuraaak.github.io/ezqt-app/getting-started/) - Installation, bootstrap, and first app
- [User Guides](https://neuraaak.github.io/ezqt-app/guides/) - Development, testing, and styling guidance
- [API Reference](https://neuraaak.github.io/ezqt-app/api/) - Service- and architecture-oriented API documentation
- [CLI Reference](https://neuraaak.github.io/ezqt-app/cli/) - Command-line utilities and command options
- [Examples](https://neuraaak.github.io/ezqt-app/examples/) - Practical usage snippets for common scenarios
- [Concepts](https://neuraaak.github.io/ezqt-app/concepts/) - Architecture rationale and design decisions

## 🖥️ CLI commands

```bash
ezqt init [--force] [--verbose] [--no-main]
ezqt create [--template basic|advanced] [--name my_app] [--verbose]
ezqt convert
ezqt docs [--serve] [--port 8000]
ezqt info
```

See the full [CLI reference](https://neuraaak.github.io/ezqt-app/cli/).

## 🧪 Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# By marker
pytest tests/ -m unit
pytest tests/ -m integration

# Coverage report
pytest tests/ --cov=src/ezqt_app --cov-report=html
```

See the [testing guide](https://neuraaak.github.io/ezqt-app/guides/testing/).

## 📋 Requirements

- Python >= 3.11
- PySide6 >= 6.7.3, < 7.0.0

## ⚖️ License

MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Links

- Repository: [github.com/neuraaak/ezqt-app](https://github.com/neuraaak/ezqt-app)
- Issues: [github.com/neuraaak/ezqt-app/issues](https://github.com/neuraaak/ezqt-app/issues)
- Documentation: [neuraaak.github.io/ezqt-app](https://neuraaak.github.io/ezqt-app/)
- PyPI: [pypi.org/project/ezqt-app](https://pypi.org/project/ezqt-app/)
- Changelog: [neuraaak.github.io/ezqt-app/changelog](https://neuraaak.github.io/ezqt-app/changelog/)
