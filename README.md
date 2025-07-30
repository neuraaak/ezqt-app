# 🚀 EzQt_App

[![Repository](https://img.shields.io/badge/Repository-GitHub-blue?style=for-the-badge&logo=github)](https://github.com/neuraaak/EzQt-App)
[![PyPI](https://img.shields.io/badge/PyPI-ezqt_app-green?style=for-the-badge&logo=pypi)](https://pypi.org/project/EzQt_App/)
[![Tests](https://img.shields.io/badge/Tests-240%2B%20passing-green?style=for-the-badge&logo=pytest)](https://github.com/neuraaak/EzQt-App/actions)

A lightweight Python framework based on PySide6 to quickly build modern desktop applications, with integrated resource, theme, and reusable component management.

## 📦 **Installation**

```bash
pip install ezqt_app
```

## 🚀 **Quick Start**

```python
import sys
import ezqt_app.main as ezqt
from ezqt_app.app import EzQt_App, EzApplication

# Initialize the framework
ezqt.init()

# Create application
app = EzApplication(sys.argv)

# Create main window
window = EzQt_App(themeFileName="main_theme.qss")

# Add menus
home_page = window.addMenu("Home", "🏠")
settings_page = window.addMenu("Settings", "⚙️")

# Show application
window.show()
app.exec()
```

## 📚 **Documentation**

- **[📖 Complete Documentation](docs/README.md)** - Main documentation guide
- **[🔧 API Documentation](docs/api/API_DOCUMENTATION.md)** - Complete documentation of all components
- **[🎨 Style Guide](docs/api/STYLE_GUIDE.md)** - QSS customization and best practices
- **[🧪 Tests](docs/tests/README.md)** - Test documentation and execution guide
- **[🖥️ CLI Documentation](docs/cli/README.md)** - Command-line interface guide
- **[📋 Changelog](CHANGELOG.md)** - Version history

## 🎯 **Available Components**

### 🧠 **Core Module (`ezqt_app.kernel`)**
- **Kernel** - Core application functions and resource management
- **TranslationManager** - Multilingual translation system
- **Settings** - Application configuration and parameters
- **FileMaker** - File and resource generation utilities

### 🎨 **Widget Module (`ezqt_app.widgets`)**
- **EzApplication** - Extended QApplication with theme support
- **EzQt_App** - Main application window with modern UI
- **Core Widgets** - Header, Menu, PageContainer, SettingsPanel
- **Extended Widgets** - SettingWidgets with validation

### 🔧 **CLI Module (`ezqt_app.cli`)**
- **CLI** - Command line interface for project management
- **ProjectRunner** - Project creation and template management
- **Create QM Files** - Translation file conversion utilities

### 🌍 **Translation Module (`ezqt_app.kernel.translation`)**
- **TranslationManager** - Complete translation management
- **Auto-Translator** - Multi-provider automatic translation system
- **String Collector** - Automatic string collection for translations
- **Translation Helpers** - Utility functions for translations
- **Translation Config** - Configuration and setup

## ✨ **Features**

- **✅ PySide6 6.9.1** - Modern Qt framework with latest features
- **✅ Automatic Generation** - Asset folders, QRC files, and resources
- **✅ Dynamic Themes** - Light/dark themes with integrated toggle
- **✅ Global Translation** - Multi-language support (EN, FR, ES, DE)
- **✅ Automatic Translation System** - Multi-provider support (LibreTranslate, MyMemory, Google)
- **✅ CLI Tools** - Project initialization and management
- **✅ Template System** - Basic and advanced project templates
- **✅ Type Annotations** - Complete type hint support
- **✅ Tests** - Comprehensive test suite (~240+ tests)
- **✅ Standardized Logging** - Consistent message formatting across all components

## 🧪 **Tests**

### **Quick Execution**
```bash
# Quick verification
python tests/run_tests.py --type unit

# Tests with coverage
python tests/run_tests.py --coverage

# Or use CLI
ezqt test --unit
ezqt test --coverage
```

### **Test Documentation**
- **[🚀 Quick Start Guide](docs/tests/QUICK_START_TESTS.md)** - Quick verification
- **[📖 Complete Documentation](docs/tests/TESTS_DOCUMENTATION.md)** - Detailed guide

### **Statistics**
- **Total** : ~240+ tests
- **Coverage** : High coverage across all modules
- **Status** : 🟢 **OPERATIONAL**

## 🖥️ **CLI Commands**

### **Project Management**
```bash
# Initialize new project
ezqt init [--force] [--verbose] [--no-main]

# Create project template
ezqt create --template <type> --name <name>

# Show project information
ezqt info
```

### **Development Tools**
```bash
# Convert translation files
ezqt convert [--verbose]
ezqt mkqm [--verbose]

# Run tests
ezqt test [--unit] [--integration] [--coverage]

# Serve documentation
ezqt docs [--serve] [--port <port>]
```

### **CLI Documentation**
- **[🖥️ Complete Guide](docs/cli/README.md)** - All commands and options

## 🌍 **Translation System**

The framework includes a complete translation system with automatic translation capabilities:

```python
from ezqt_app.kernel import tr, set_tr

# Translate text
text = tr("Hello World")  # Returns "Bonjour le monde" in French

# Set translated text for widget
from PySide6.QtWidgets import QLabel
label = QLabel("Hello World")
set_tr(label, "Hello World")  # Automatically retranslates on language change

# Change language
from ezqt_app.kernel import change_language
change_language("Français")  # Automatically retranslates all registered widgets

# Automatic translation (when enabled)
from ezqt_app.kernel.translation.auto_translator import AutoTranslator
translator = AutoTranslator()
auto_translated = translator.translate_sync("Hello World", "fr")
```

**Supported languages:** English, Français, Español, Deutsch  
**Translation providers:** LibreTranslate, MyMemory, Google Translate  
**Note:** Automatic translation system is temporarily disabled for development

## 🎨 **Template System**

### **Basic Template**
```bash
ezqt create --template basic --name my_app
```

**Structure:**
```
my_app/
├── main.py              # Application entry point
├── assets/              # Application assets
│   ├── icons/          # Icon files
│   ├── images/         # Image files
│   └── themes/         # QSS theme files
└── README.md           # Project documentation
```

### **Advanced Template**
```bash
ezqt create --template advanced --name my_app
```

**Structure:**
```
my_app/
├── main.py              # Advanced application entry point
├── assets/              # Application assets
├── src/                 # Source code
│   ├── widgets/        # Custom widgets
│   └── utils/          # Utility functions
├── tests/              # Test files
├── docs/               # Documentation
└── README.md           # Project documentation
```

## 🔧 **Development**

### **Project Structure**
```
ezqt_app/
├── README.md                    # This file
├── docs/                        # Documentation
│   ├── README.md               # Documentation index
│   ├── api/                    # API documentation
│   │   ├── README.md          # Navigation guide
│   │   ├── API_DOCUMENTATION.md # Complete documentation
│   │   └── STYLE_GUIDE.md     # Style guide
│   ├── cli/                    # CLI documentation
│   │   └── README.md          # CLI guide
│   └── tests/                  # Test documentation
│       ├── README.md          # Navigation guide
│       ├── TESTS_DOCUMENTATION.md # Complete documentation
│       └── QUICK_START_TESTS.md # Quick start guide
├── tests/                       # Tests
│   ├── run_tests.py           # Test execution script
│   ├── conftest.py            # Pytest configuration
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── ezqt_app/                   # Source code
│   ├── kernel/                # Core components
│   ├── widgets/               # Custom widgets
│   ├── cli/                   # Command line interface
│   └── resources/             # Embedded resources
└── pyproject.toml              # Project configuration
```

### **Development Installation**
```bash
git clone https://github.com/neuraaak/EzQt-App.git
cd ezqt_app
pip install -e ".[dev]"

# Verify CLI installation
ezqt --version
ezqt info
```

## 📦 **Dependencies**

### **Main Dependencies**
- **PySide6==6.9.1** - Modern Qt framework
- **PyYaml==6.0.2** - YAML file management
- **colorama==0.4.6** - Terminal colors
- **requests==2.32.3** - HTTP requests
- **click>=8.0.0** - CLI framework
- **ezqt-widgets>=2.0.0** - Custom widgets

### **Development Dependencies**
- **pytest>=7.0.0** - Testing framework
- **pytest-cov>=4.0.0** - Coverage reporting
- **pytest-qt>=4.0.0** - Qt testing
- **pytest-mock>=3.10.0** - Mocking utilities
- **flake8>=5.0.0** - Code linting
- **black>=22.0.0** - Code formatting

## 🎨 **Customization**

### **Themes**
```css
/* Custom QSS theme */
QMainWindow {
    background-color: #2d2d2d;
    color: #ffffff;
}

QPushButton {
    background-color: #0078d4;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    color: white;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106ebe;
}
```

### **Custom Widgets**
```python
from ezqt_app.widgets.core.header import Header
from ezqt_app.widgets.core.menu import Menu
from ezqt_app.widgets.extended.setting_widgets import SettingWidgets

# Create custom widgets
header = Header()
menu = Menu()
settings = SettingWidgets()
```

## 📄 **License**

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**EzQt_App** - Modern framework for Qt applications with PySide6 6.9.1 🚀
