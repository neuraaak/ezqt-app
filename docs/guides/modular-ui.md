# Modular UI guide

EzQt_App v5.3.0 introduced a modular UI system that lets you enable or disable core
components (the left menu and the settings panel) using a fluent builder API.

## 🔧 The builder pattern

UI construction is decoupled from class instantiation. Call `.build()` explicitly
to generate the layout:

```python
from ezqt_app import EzQt_App

# Standard initialization — menu and settings panel both enabled
window = EzQt_App().build()
```

## 🎛️ Disabling components

### Disabling the left menu

```python
# Application window without the left sidebar
window = EzQt_App().no_menu().build()
```

### Disabling the settings panel

```python
# Application window without the right settings panel
window = EzQt_App().no_settings_panel().build()
```

### Combining options

Chain methods to create a minimal shell with only the header and content area:

```python
window = (
    EzQt_App()
    .no_menu()
    .no_settings_panel()
    .build()
)
```

## 🏗️ Implementation details

### Null object pattern

When a component is disabled, `EzQt_App` injects a null object implementation
(e.g., `NullMenuContainer`, `NullSettingsPanel`). These objects:

- Satisfy the internal protocols and contracts.
- Occupy 0 px of space in the layout.
- Perform no-op operations for method calls.

This ensures that services (Translation, Theme, etc.) can still interact with
these components without requiring `if window.ui.menu_container is not None`
checks throughout the codebase.

### Backward compatibility

Calling `show()` on an instance where `.build()` has not been called will
trigger `build()` automatically. However, calling `.build()` explicitly is
strongly recommended for clarity and to enable the modular options.

```python
# Legacy style (still works — build() is triggered implicitly by show())
window = EzQt_App()
window.show()
```

!!! warning "Implicit build is deprecated"
    Relying on `show()` to trigger `build()` will be removed in a future
    version. Always call `.build()` explicitly.

## ➡️ See also

- [API Reference — Application Layer](../api/reference/application.md) — `EzQt_App` full API
- [Getting Started](../getting-started.md) — step-by-step first app
- [Examples](../examples/index.md) — copy-paste snippets
