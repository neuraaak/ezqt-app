# UI services and widgets

UI orchestration services and reusable widget containers.

## 📡 Theme signal integration

`EzQt_App` emits `themeChanged` whenever the active theme is switched via
the settings panel flow (`set_app_theme()` / `refresh_theme()`).

Use this signal to refresh custom widgets that keep theme-dependent caches
outside standard QSS repaint behavior.

```python
from ezqt_app import EzQt_App

window = EzQt_App().build()

def on_theme_changed() -> None:
    # Recompute theme-dependent resources in custom components.
    ...

window.themeChanged.connect(on_theme_changed)
```

## 📦 ThemeService

::: ezqt_app.services.ui.theme_service.ThemeService

## 📦 MenuService

::: ezqt_app.services.ui.menu_service.MenuService

## 📦 PanelService

::: ezqt_app.services.ui.panel_service.PanelService

## 📦 WindowService

::: ezqt_app.services.ui.window_service.WindowService

## 📦 UiComponentFactory

::: ezqt_app.services.ui.component_factory.UiComponentFactory

## 📦 Core widgets

::: ezqt_app.widgets.core.ez_app.EzApplication

::: ezqt_app.widgets.core.header.Header

::: ezqt_app.widgets.core.menu.Menu

::: ezqt_app.widgets.core.page_container.PageContainer

::: ezqt_app.widgets.core.settings_panel.SettingsPanel

## 📦 Extended widgets

::: ezqt_app.widgets.extended.setting_widgets
