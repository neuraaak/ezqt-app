# Examples

Self-contained, copy-paste snippets for the most common **EzQt App** workflows.

!!! tip
    All examples assume the package is installed: `pip install ezqt-app`

## 🚀 Bootstrap and launch

Minimal application lifecycle — the complete runnable skeleton:

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init(mk_theme=True)
app = EzApplication(sys.argv)
window = EzQt_App().build()
window.show()
sys.exit(app.exec())
```

## 💡 Bootstrap with options

Control what gets generated during initialization:

```python
from ezqt_app import init

# Generate all assets (theme, config, translations) with verbose output
summary = init(mk_theme=True, verbose=True)
print(summary)

# Place generated assets under binaries/ instead of the default bin/
summary = init(bin_path="binaries")
```

## 💡 Add pages to the app shell

Register menus at startup to populate the sidebar:

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App().build()

home_page = window.add_menu("Home", "home")
settings_page = window.add_menu("Settings", "settings")
analytics_page = window.add_menu("Analytics", "analytics")

window.refresh_theme()
window.show()
sys.exit(app.exec())
```

## 💡 Access app icons and images after bootstrap

`AppIcons` and `AppImages` are populated by `init()`. Always import them after
`init()` has run:

```python
from ezqt_app import init
from ezqt_app.shared.resources import AppIcons, AppImages

init()  # generates bin/app_icons.py and bin/app_images.py

icon_path = AppIcons.cil_home           # ":/icons/cil-home.png"
logo_path = AppImages.logo_placeholder  # ":/images/logo-placeholder.jpg"
```

!!! warning "Import order matters"
    Importing `AppIcons` or `AppImages` at module top-level **before** `init()` runs
    captures `None` — the variable is never updated. Always call `init()` first, or
    access symbols through the module object:

    ```python
    from ezqt_app.shared import resources

    init()
    icon_path = resources.AppIcons.cil_home  # always resolves to the live value
    ```

## 💡 Change language at runtime

Switch the application language programmatically:

```python
from ezqt_app.services.translation import change_language_by_code

# Switch to French
change_language_by_code("fr")

# Switch back to English
change_language_by_code("en")
```

## 💡 Disable auto-translation

Keep local `.ts` support while disabling external API calls:

```python
window = EzQt_App().build()
window.enable_auto_translation(False)
window.show()
```

## 💡 Apply a custom theme

All `.qss` files under `bin/themes/` are loaded automatically — no file name
needs to be passed explicitly:

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App().build()  # themes loaded from bin/themes/ automatically
window.show()
sys.exit(app.exec())
```

## 💡 Read configuration at runtime

```python
from ezqt_app.services.settings import get_settings_service

settings = get_settings_service()
theme = settings.get("theme", default="dark")
language = settings.get("language", default="en")
```

## 💡 Full app with pages and language switch

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init
from ezqt_app.services.translation import change_language_by_code


class MyApp:
    def __init__(self):
        init(mk_theme=True, verbose=False)
        self.app = EzApplication(sys.argv)
        self.window = EzQt_App().build()

        self.window.add_menu("Dashboard", "dashboard")
        self.window.add_menu("Reports", "reports")
        self.window.add_menu("Settings", "settings")

        change_language_by_code("fr")

    def run(self) -> int:
        self.window.show()
        return self.app.exec()


if __name__ == "__main__":
    app = MyApp()
    sys.exit(app.run())
```

## ➡️ Related

- [Getting Started](../getting-started.md) — step-by-step first app tutorial
- [API Reference](../api/index.md) — full service and widget documentation
- [CLI Reference](../cli/index.md) — all `ezqt` commands
- [QSS style guide](../guides/style-guide.md) — theme and widget styling
