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

Use `bin_path` to place generated assets in a directory other than the default `bin/`:

```python
from ezqt_app import init

# Assets will be generated under <project_root>/binaries/ instead of bin/
init(bin_path="binaries")
```

The path is resolved relative to `project_root` (defaults to `Path.cwd()`).

---

## Run a Basic App

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App().build()
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
window = EzQt_App().build()
window.enable_auto_translation(False)
window.set_app_theme()
```

### Add Pages and Refresh Theme

When you add widgets after `build()`, call `refresh_theme()` so that QSS rules
targeting `#objectName` selectors are evaluated against the new widgets:

```python
window = EzQt_App().build()
window.show()
home_page = window.add_menu("Home", "home")
settings_page = window.add_menu("Settings", "settings")
window.refresh_theme()
```

### Add Pages to App Shell

```python
window = EzQt_App().build()
home_page = window.add_menu("Home", "home")
settings_page = window.add_menu("Settings", "settings")
window.show()
```

---

## QSS and Theming

EzQt App uses a QSS-based theming workflow. All `.qss` files placed under
`bin/themes/` in your bootstrapped project are loaded automatically at runtime —
no explicit file name is required:

```python
window = EzQt_App().build()
```

The theme directory ships with three files loaded in alphabetical order:

| File                         | Scope                    |
| ---------------------------- | ------------------------ |
| `bin/themes/application.qss` | Application-level styles |
| `bin/themes/extended.qss`    | EzQt extended widgets    |
| `bin/themes/global.qss`      | Standard Qt widgets      |

The active theme preset is stored in settings as `THEME_PRESET` and `THEME`
(format: `"preset:variant"`, e.g. `"blue-gray:dark"`). Available presets are
read dynamically from `theme.config.yaml` via `ThemeService.get_available_themes()`.

!!! warning "Deprecated argument"
Passing `theme_file_name` to `EzQt_App()` still compiles but emits a
deprecation warning and has no effect. Remove it from your code.

See the [QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/) for conventions and per-component examples.

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

### `pyside6-rcc` Not Found

If `pyside6-rcc` is missing from your environment, `init()` raises a
`ResourceCompilationError` instead of silently skipping QRC compilation:

```python
ezqt_app.domain.errors.ResourceCompilationError: pyside6-rcc not found
```

**Solution** — ensure PySide6 tools are installed and on `PATH`:

```bash
pip install PySide6
# or, in a virtual environment, verify the executable is available:
python -m PySide6.scripts.pyside6_tool rcc --version
```

If you are in a corporate environment installing from wheel files, make sure
the PySide6 tools wheel (`PySide6_Essentials` or `PySide6_Addons`) is also
installed alongside the main package.

---

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
