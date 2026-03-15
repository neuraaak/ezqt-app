# Examples

Usage examples and scenarios for **ezqt_app** workflows.

---

## Overview

EzQt App focuses on project bootstrap and app-shell composition. Examples below cover the most common workflows.

---

## Available Example Scenarios

| Scenario          | Description                            | Related API                    |
| ----------------- | -------------------------------------- | ------------------------------ |
| Bootstrap project | Generate app/config/theme/translations | `ezqt init`, `init(...)`       |
| Start app shell   | Create and show `EzQt_App` window      | `EzApplication`, `EzQt_App`    |
| Manage language   | Switch language and register UI text   | translation helpers            |
| Theme workflow    | Apply and switch theme at runtime      | `ThemeService`, settings panel |

---

## Running Examples

### With Python

```bash
python -c "from ezqt_app import init; print(init())"
```

### With CLI

```bash
ezqt init --verbose
ezqt test --unit
ezqt docs --serve
```

---

## Code Examples

### Bootstrap and Launch

Minimal application lifecycle:

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init(mk_theme=True)
app = EzApplication(sys.argv)
window = EzQt_App()
window.show()
sys.exit(app.exec())
```

### Bootstrap with Options

Control what gets generated during initialization:

```python
from ezqt_app import init

# Generate all assets (theme, config, translations)
summary = init(mk_theme=True, verbose=True)
print(summary)

# Skip main.py generation
summary = init(no_main=True)
```

### Add Pages to the App Shell

Register menus/pages at startup:

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App()

home_page = window.add_menu("Home", "home")
settings_page = window.add_menu("Settings", "settings")
analytics_page = window.add_menu("Analytics", "analytics")

window.show()
sys.exit(app.exec())
```

### Change Language at Runtime

Switch the application language programmatically:

```python
from ezqt_app.services.translation import change_language_by_code

# Switch to French
change_language_by_code("fr")

# Switch back to English
change_language_by_code("en")
```

### Disable Auto-Translation

Control whether external translation providers are called:

```python
window = EzQt_App()

# Disable external API calls while keeping local TS support
window.enable_auto_translation(False)

window.show()
```

### Apply a Custom Theme

Load a custom QSS theme file at startup:

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App(theme_file_name="my_custom_theme.qss")
window.show()
sys.exit(app.exec())
```

### Access Config Service

Read configuration values at runtime:

```python
from ezqt_app.services.settings import get_settings_service

settings = get_settings_service()
theme = settings.get("theme", default="dark")
language = settings.get("language", default="en")
```

---

## Advanced Example: Full App with Pages and Language Switch

```python
import sys
from PySide6.QtWidgets import QApplication
from ezqt_app import EzApplication, EzQt_App, init
from ezqt_app.services.translation import change_language_by_code


class MyApp:
    def __init__(self):
        init(mk_theme=True, verbose=False)
        self.app = EzApplication(sys.argv)
        self.window = EzQt_App(theme_file_name="main_theme.qss")

        # Register pages
        self.window.add_menu("Dashboard", "dashboard")
        self.window.add_menu("Reports", "reports")
        self.window.add_menu("Settings", "settings")

        # Start in French
        change_language_by_code("fr")

    def run(self) -> int:
        self.window.show()
        return self.app.exec()


if __name__ == "__main__":
    app = MyApp()
    sys.exit(app.run())
```

---

## Suggested Real-World Scenarios

- Bootstrap a new desktop project with `ezqt init`
- Add pages with `EzQt_App.add_menu(...)`
- Customize themes using `bin/themes/main_theme.qss`
- Switch UI language using translation service helpers
- Run tests by scope with `python tests/run_tests.py --type unit`

---

## Related

- [Getting Started](https://neuraaak.github.io/ezqt-app/getting-started/)
- [API Reference](https://neuraaak.github.io/ezqt-app/api/)
- [CLI Reference](https://neuraaak.github.io/ezqt-app/cli/)
- [QSS Style Guide](https://neuraaak.github.io/ezqt-app/guides/style-guide/)
