# Modular UI Guide

EzQt_App v5.3.0 introduced a modular UI system that allows you to enable or disable core components like the left menu and the settings panel using a fluent API.

## The Builder Pattern

To support modularity, UI construction is now decoupled from class instantiation. You must explicitly call `.build()` to generate the UI layout.

### Basic Usage

```python
from ezqt_app import EzQt_App

# Standard initialization (Menu and Settings enabled)
window = EzQt_App().build()
```

## Disabling Components

You can use the fluent API to customize which components are included in your application window.

### Disabling the Left Menu

If your application doesn't need a sidebar menu, you can disable it using `.no_menu()`:

```python
# Create an app window without the left sidebar
window = EzQt_App().no_menu().build()
```

### Disabling the Settings Panel

To remove the slide-in settings panel and hide its corresponding button in the header, use `.no_settings_panel()`:

```python
# Create an app window without the right settings panel
window = EzQt_App().no_settings_panel().build()
```

### Combining Options

You can chain these methods to create a minimal "shell" application:

```python
# Minimal window with only Header, Content Area, and Bottom Bar
window = (
    EzQt_App()
    .no_menu()
    .no_settings_panel()
    .build()
)
```

## Implementation Details

### Null Object Pattern

When a component is disabled, EzQt_App injects a **Null Object** implementation (e.g., `NullMenuContainer`, `NullSettingsPanel`). These objects:

- Satisfy the internal protocols and contracts.
- Occupy 0px of space in the layout.
- Perform no-op operations for method calls.

This ensures that services (like the Translation or Theme services) can still "talk" to these components without needing complex `if window.ui.menu_container is not None` checks throughout the codebase.

### Backward Compatibility

For existing applications, calling `show()` will automatically trigger `build()` if it hasn't been called yet. However, it is **strongly recommended** to use the explicit `.build()` call for clarity and to enable the modular options.

```python
# Legacy style (still works, but build() is implicit)
window = EzQt_App()
window.show()
```
