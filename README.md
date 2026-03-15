# 🚀 EzQt App

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/OS-Independent-lightgray.svg?style=for-the-badge)](https://pypi.org/project/ezqt-app/)
[![Version](https://img.shields.io/badge/Version-5.3.0-orange.svg?style=for-the-badge)](https://pypi.org/project/ezqt-app/)
[![PyPI](https://img.shields.io/badge/PyPI-ezqt--app-green.svg?style=for-the-badge&logo=pypi)](https://pypi.org/project/ezqt-app/)
[![Docs](https://img.shields.io/badge/Docs-Online-blue.svg?style=for-the-badge&logo=readthedocs)](https://neuraaak.github.io/ezqt-app/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Beta-yellow.svg?style=for-the-badge)](https://github.com/neuraaak/ezqt-app)
[![Tests](https://img.shields.io/badge/Tests-426%2B%20passing-success.svg?style=for-the-badge)](https://github.com/neuraaak/ezqt-app)

![EzQt Widgets Logo](docs/assets/logo-min.png)

**EzQt App** is a lightweight Python framework based on **PySide6** to quickly build modern desktop applications, with integrated resource, theme, translation, and reusable component management. Built on a hexagonal architecture for clean separation of concerns.

## 📦 Installation

```bash
pip install ezqt-app
```

Or from source:

```bash
git clone https://github.com/neuraaak/ezqt-app.git
cd ezqt-app && pip install .
```

## 🚀 Quick Start

```python
import sys
from ezqt_app.app import EzQt_App
from ezqt_app.services.application.app_service import AppService

# Initialize and run the framework
app_service = AppService()
app_service.initialize()

# Create main window
window = EzQt_App(themeFileName="main_theme.qss")

# Add navigation menus
home_page = window.addMenu("Home", "🏠")
settings_page = window.addMenu("Settings", "⚙️")

# Show application
window.show()
app_service.exec()
```

## 🎯 Key Features

- **✅ PySide6 Compatible**: Full support for the latest PySide6 versions
- **✅ Hexagonal Architecture**: Clean domain/services/widgets separation
- **✅ Full Type Hints**: Complete typing support for IDEs and linters
- **✅ Dynamic Themes**: Light/dark themes with integrated toggle via QSS
- **✅ Global Translation**: Multi-language support (EN, FR, ES, DE)
- **✅ Automatic Translation**: Non-blocking multi-provider system (Google, MyMemory, LibreTranslate) with daemon-thread HTTP, in-flight deduplication, and progressive `.ts`/`.qm` file population
- **✅ CLI Tools**: Project initialization, template generation, and management
- **✅ Template System**: Basic and advanced project scaffolding
- **✅ Standardized Logging**: Consistent message formatting across all components
- **✅ Comprehensive Tests**: Complete test suite (~426 tests)

## 📚 Documentation

Full documentation is available online: **[neuraaak.github.io/ezqt-app](https://neuraaak.github.io/ezqt-app/)**

- **[📖 Getting Started](https://neuraaak.github.io/ezqt-app/getting-started/)** – Installation and first steps
- **[🎯 API Reference](https://neuraaak.github.io/ezqt-app/api/)** – Complete module reference (auto-generated)
- **[🎨 QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/)** – QSS customization and best practices
- **[💡 Examples](https://neuraaak.github.io/ezqt-app/examples/)** – Usage examples and demonstrations
- **[🖥️ CLI](https://neuraaak.github.io/ezqt-app/cli/)** – Command-line interface guide
- **[🧪 Testing](https://neuraaak.github.io/ezqt-app/guides/testing/)** – Test suite documentation
- **[🔧 Development](https://neuraaak.github.io/ezqt-app/guides/development/)** – Environment setup and contribution

## 🏗️ Architecture

EzQt App follows a **hexagonal architecture** with three main layers:

```text
src/ezqt_app/
├── domain/          # Contracts, ports, models, errors (no dependencies)
│   ├── ports/       # Abstract interfaces (AppPort, ConfigPort, etc.)
│   ├── models/      # Domain models
│   └── errors/      # Domain exceptions
├── services/        # Adapters implementing domain ports
│   ├── application/ # App lifecycle (AppService, InitService)
│   ├── config/      # Configuration (ConfigService, SettingsService)
│   ├── translation/ # i18n (TranslationService, AutoTranslator)
│   └── ui/          # UI coordination (ThemeService, MenuService)
├── widgets/         # PySide6 presentation layer
│   ├── core/        # Header, Menu, PageContainer
│   └── extended/    # SettingWidgets and advanced components
├── shared/          # Cross-cutting utilities
├── cli/             # Command-line interface
└── app.py           # Main EzQt_App entry point
```

## 🧩 Available Components

### 🔧 Application Services (`ezqt_app.services`)

| Service                 | Description                          |
| ----------------------- | ------------------------------------ |
| **AppService**          | Application lifecycle management     |
| **InitService**         | Startup initialization and bootstrap |
| **ConfigService**       | Application configuration management |
| **SettingsService**     | User settings persistence            |
| **RuntimeStateService** | Runtime state tracking               |
| **TranslationService**  | Language management and switching    |
| **ThemeService**        | Theme loading and switching          |
| **MenuService**         | Navigation menu management           |
| **WindowService**       | Main window orchestration            |

### 🌍 Translation System (`ezqt_app.services.translation`)

| Component              | Description                                                |
| ---------------------- | ---------------------------------------------------------- |
| **TranslationManager** | Central translation registry, `.ts`/`.qm` lifecycle        |
| **EzTranslator**       | Qt interceptor — feeds unknown strings to auto-translation |
| **AutoTranslator**     | Non-blocking multi-provider translation (daemon threads)   |
| **StringCollector**    | Automatic string discovery for translation                 |

### 🎨 Widgets (`ezqt_app.widgets`)

| Widget             | Description                                |
| ------------------ | ------------------------------------------ |
| **EzQt_App**       | Main application window with modern UI     |
| **Header**         | Top navigation bar with title and controls |
| **Menu**           | Sidebar navigation menu                    |
| **PageContainer**  | Content area manager                       |
| **SettingWidgets** | Settings UI components with validation     |

## 🧪 Testing

Comprehensive test suite with 426+ test cases covering services, widgets, and integration scenarios.

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run by marker
pytest tests/ -m unit
pytest tests/ -m integration

# With coverage
pytest tests/ --cov=src/ezqt_app --cov-report=html

# Using CLI
ezqt test --unit
ezqt test --coverage
```

See the **[Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/)** for complete details.

## 🖥️ CLI Commands

### Project Management

```bash
# Initialize new project (assets, QRC, resources)
ezqt init [--force] [--verbose] [--no-main]

# Create project from template
ezqt create --template basic --name my_app
ezqt create --template advanced --name my_app

# Show project information
ezqt info
```

### Development Tools

```bash
# Convert .ts translation files to .qm
ezqt convert [--verbose]
ezqt mkqm [--verbose]

# Run tests
ezqt test [--unit] [--integration] [--coverage]

# Serve documentation
ezqt docs [--serve] [--port <port>]
```

## 🌍 Translation System

```python
# Use Qt's standard translation call — EzTranslator intercepts automatically
from PySide6.QtCore import QCoreApplication
text = QCoreApplication.translate("EzQt_App", "Hello World")

# Change active language (triggers LanguageChange on all widgets)
from ezqt_app.services.translation import get_translation_manager
get_translation_manager().load_language("Français")

# Enable auto-translation: unknown strings are translated via external providers
# and progressively saved to .ts files, then compiled to .qm
window.enable_auto_translation(True)
```

**Supported languages:** English, Français, Español, Deutsch
**Translation providers:** Google Translate, MyMemory, LibreTranslate (tried in order, daemon threads — UI never blocked)
**Auto-populate:** `.ts` files are updated at runtime; `.qm` files are recompiled via `pyside6-lrelease` on each language load. Identity entries are written for the source language so `en.ts` is always populated.

## 🛠️ Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/neuraaak/ezqt-app.git
cd ezqt-app
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify CLI installation
ezqt --version
ezqt info
```

See the **[Development Guide](https://neuraaak.github.io/ezqt-app/guides/development/)** for detailed instructions.

## 📦 Dependencies

### Runtime

- **PySide6>=6.7.3** – Qt for Python framework
- **requests>=2.32.4** – HTTP requests (translation providers)
- **click>=8.2.1** – CLI framework
- **PyYAML>=6.0** – YAML configuration
- **ruamel.yaml==0.18.6** – Advanced YAML processing

### Development

- **pytest>=7.0.0** – Testing framework
- **pytest-cov>=4.0.0** – Coverage reporting
- **ruff>=0.1.0** – Linting and formatting
- **mypy / pyright** – Type checking

## 📄 License

MIT License – See [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: [https://github.com/neuraaak/ezqt-app](https://github.com/neuraaak/ezqt-app)
- **Issues**: [GitHub Issues](https://github.com/neuraaak/ezqt-app/issues)
- **Documentation**: [neuraaak.github.io/ezqt-app](https://neuraaak.github.io/ezqt-app/)
- **PyPI**: [pypi.org/project/ezqt-app](https://pypi.org/project/ezqt-app/)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

**EzQt App** – Modern PySide6 application framework with hexagonal architecture. 🚀
