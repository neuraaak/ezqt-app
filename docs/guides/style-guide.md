# QSS style guide

Practical QSS style conventions for EzQt App components.

## ⚙️ General principles

- Use consistent colors, spacing, and borders across all core containers.
- Prefer specific object names (`#settings_panel`, `#menu_container`, etc.).
- Centralize palette values in theme/config files whenever possible.

## 📁 Where styles come from

All `.qss` files found in `bin/themes/` are loaded automatically at application
startup in alphabetical order. The directory ships with three files:

| File                         | Scope                                                       |
| :--------------------------- | :---------------------------------------------------------- |
| `bin/themes/application.qss` | Application-level styles (window chrome, layout containers) |
| `bin/themes/extended.qss`    | EzQt extended widgets (`OptionSelector`, `ThemeIcon`, etc.) |
| `bin/themes/global.qss`      | Standard Qt widgets (`QPushButton`, `QLineEdit`, etc.)      |

To add project-specific styles, place an additional `.qss` file in the same
directory. It will be picked up automatically on the next run.

Additional sources:

- Resource defaults bundled in the package
- Runtime application orchestrated by `ThemeService`

## 🎨 Theme previews

The three built-in themes ship with a color palette preview.
Select a theme in the settings panel at runtime, or set `settings_panel.theme.default`
in `bin/config/app.config.yaml`.

### Blue Gray

<div>
--8<-- "src/ezqt_app/resources/themes/preview/blue-gray-preview.html"
</div>

### GitHub Dark

<div>
--8<-- "src/ezqt_app/resources/themes/preview/github-dark-preview.html"
</div>

### Warm Dark

<div>
--8<-- "src/ezqt_app/resources/themes/preview/warm-dark-preview.html"
</div>

## 🏗️ Core containers

### Main window

```css
QMainWindow {
  background: #20242b;
  color: #e7ecf3;
}
```

### Settings panel

```css
QFrame#settings_panel {
  border-left: 1px solid #2f3640;
  background: #262b33;
}
```

### Menu container

```css
QFrame#menu_container {
  background: #1d222a;
  border-right: 1px solid #2f3640;
}
```

## 🎨 Interactive controls

### Hover/focus baseline

```css
QPushButton:hover,
QToolButton:hover {
  border-color: #4c5a6f;
}

QPushButton:focus,
QLineEdit:focus {
  border-color: #3b82f6;
}
```

### Theme selector pattern

```css
[type="OptionSelector_Selector"] {
  background: #3b82f6;
  border-radius: 6px;
}
```

### Settings button open state

The settings button in the header receives a dynamic `open` property whose
value is `"true"` when the settings panel is visible and `"false"` when it is
hidden. Use this to give the button a distinct active appearance:

```css
QPushButton#settings_btn[open="true"] {
  background: var(--accent_brand);
  border-color: var(--accent_brand);
}

QPushButton#settings_btn[open="false"] {
  background: transparent;
}
```

## ✅ Best practices

- Keep theme tokens centralized in config/theme files.
- Avoid hardcoding colors in widget code when possible.
- Prefer object names for targeted QSS rules.
- Keep dark/light variants symmetrical when possible.
- Validate styles on both Windows and Linux runtimes.
- Keep transitions/animations meaningful and unobtrusive.

## ➡️ Related

- `src/ezqt_app/services/ui/theme_service.py`
- `src/ezqt_app/widgets/core/settings_panel.py`
- [Qt resources pipeline](resources.md) — how themes are compiled and loaded
