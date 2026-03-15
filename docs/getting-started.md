# Getting Started

This guide will help you get started with **EzQt App** quickly and easily.

## Installation

### From PyPI (Recommended)

```bash
pip install ezqt-app
```

### From Source

```bash
git clone https://github.com/neuraaak/ezqt-app.git
cd ezqt_app
pip install .
```

### Development Installation

For contributors and maintainers:

```bash
pip install -e ".[dev]"
```

This installs EzQt App in editable mode with development dependencies.

---

## Requirements

- **Python** >= 3.10
- **PySide6** >= 6.7.3
- **PyYAML / ruamel.yaml** – Configuration management

---

## First Steps

### Bootstrap a Project

From your project root:

```bash
ezqt init
```

Useful options:

```bash
ezqt init --verbose
ezqt init --force
ezqt init --no-main
```

### Alternative Python API Bootstrap

```python
from ezqt_app import init

summary = init(mk_theme=True, verbose=True)
print(summary)
```

---

## Run a Basic App

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App(theme_file_name="main_theme.qss")
window.show()
sys.exit(app.exec())
```

---

## Imports

Primary imports are available at package root:

```python
from ezqt_app import EzApplication, EzQt_App, init
```

Or from targeted modules:

```python
from ezqt_app.services.settings import get_settings_service
from ezqt_app.services.translation import get_translation_service
```

---

## Common Operations

### Change Language

```python
from ezqt_app.services.translation import change_language_by_code

change_language_by_code("fr")
```

### Toggle Theme in App

```python
window = EzQt_App()
window.enable_auto_translation(False)
window.set_app_theme()
```

### Add Pages to App Shell

```python
window = EzQt_App()
home_page = window.add_menu("Home", "home")
settings_page = window.add_menu("Settings", "settings")
window.show()
```

---

## QSS and Theming

EzQt App uses a QSS-based theming workflow. Theme files are loaded at runtime:

```python
window = EzQt_App(theme_file_name="main_theme.qss")
```

Theme files live in `bin/themes/` in your bootstrapped project. See the
[QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/) for conventions and per-component examples.

---

## Run Tests

```bash
python tests/run_tests.py --type unit
python tests/run_tests.py --type integration
python tests/run_tests.py --type robustness
python tests/run_tests.py --coverage
```

`tests/run_tests.py` streams pytest output in real time.

### CLI Alternative

```bash
ezqt test --unit
ezqt test --integration
ezqt test --coverage
```

---

## Next Steps

Now that you have EzQt App running, explore these resources:

- **[API Reference](https://neuraaak.github.io/ezqt-app/api/)** – Service- and architecture-oriented API documentation
- **[Examples](https://neuraaak.github.io/ezqt-app/examples/)** – Practical usage snippets for common scenarios
- **[QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/)** – Theme and widget styling conventions
- **[User Guides](https://neuraaak.github.io/ezqt-app/guides/)** – Development, testing, and styling guidance
- **[Testing Guide](https://neuraaak.github.io/ezqt-app/guides/testing/)** – Test suite scopes and how to run them
- **[Development Guide](https://neuraaak.github.io/ezqt-app/guides/development/)** – Set up your development environment and contribute
- **[CLI Reference](https://neuraaak.github.io/ezqt-app/cli/)** – Command-line utilities and command options

---

## Troubleshooting

### Import Error

```python
# Make sure you're importing from 'ezqt_app', not 'ezqt-app'
from ezqt_app import EzApplication  # Correct
```

### PySide6 Installation Issues

```bash
# Upgrade pip first
pip install --upgrade pip

# Then install PySide6
pip install PySide6>=6.7.3

# Or install with wheel file (corporate environments)
pip install path/to/PySide6-6.7.3-cp310-cp310-win_amd64.whl
```

### Missing Config or Assets After `init`

If config files or assets are missing after bootstrap:

```bash
# Re-run init (use --force to overwrite existing files)
ezqt init --force --verbose
```

### CLI Command Not Found

```bash
# Reinstall in editable mode
pip install -e ".[dev]"

# Verify the entry point is available
ezqt --version
```

### Qt Import Errors

```python
# Verify PySide6 is available
python -c "import PySide6; print(PySide6.__version__)"
```

---

## Need Help?

- **Documentation**: [Full API Reference](https://neuraaak.github.io/ezqt-app/api/)
- **Examples**: [Code Examples](https://neuraaak.github.io/ezqt-app/examples/)
- **Issues**: [GitHub Issues](https://github.com/neuraaak/ezqt-app/issues)
- **Repository**: [https://github.com/neuraaak/ezqt-app](https://github.com/neuraaak/ezqt-app)

---

**Ready to build structured PySide6 applications!**
