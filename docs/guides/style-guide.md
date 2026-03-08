# QSS Style Guide

This document defines practical QSS style conventions for EzQt App components.

## General Principles

- Use consistent colors, spacing, and borders across all core containers.
- Prefer specific object names (`#settingsPanel`, `#menuContainer`, etc.).
- Centralize palette values in theme/config files whenever possible.

---

## Where Styles Come From

- Theme files in runtime project: `bin/themes/*.qss`
- Resource defaults in package resources
- Runtime application through `ThemeService`

---

## Core Containers

### Main Window

```css
QMainWindow {
  background: #20242b;
  color: #e7ecf3;
}
```

### Settings Panel

```css
QFrame#settingsPanel {
  border-left: 1px solid #2f3640;
  background: #262b33;
}
```

### Menu Container

```css
QFrame#menuContainer {
  background: #1d222a;
  border-right: 1px solid #2f3640;
}
```

---

## Interactive Controls

### Hover/Focus Baseline

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

### Theme Selector Pattern

```css
[type="OptionSelector_Selector"] {
  background: #3b82f6;
  border-radius: 6px;
}
```

---

## Practical Recommendations

- Keep theme tokens centralized in config/theme files.
- Avoid hardcoding colors in widget code when possible.
- Prefer object names for targeted QSS rules.

---

## Best Practices

- Keep dark/light variants symmetrical when possible.
- Validate styles on both Windows and Linux runtimes.
- Keep transitions/animations meaningful and unobtrusive.

## Related Components

- `src/ezqt_app/services/ui/theme_service.py`
- `src/ezqt_app/widgets/core/settings_panel.py`
