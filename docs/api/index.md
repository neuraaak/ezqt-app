# API Reference

Complete API reference for **EzQt App**.

## Overview

EzQt App API is organized by architectural responsibility rather than by widget families.

## Quick Reference

| Component                                                                           | Description                              | Documentation                   |
| ----------------------------------------------------------------------------------- | ---------------------------------------- | ------------------------------- |
| [Application Layer](https://neuraaak.github.io/ezqt-app/api/reference/application/) | Main app shell and bootstrap entrypoints | Initialization and runtime flow |
| [Config and Runtime](https://neuraaak.github.io/ezqt-app/api/reference/config/)     | Configuration and mutable runtime state  | Config, settings, runtime ports |
| [Translation](https://neuraaak.github.io/ezqt-app/api/reference/translation/)       | Translation manager and auto-translation | Language, TS, providers         |
| [UI Services and Widgets](https://neuraaak.github.io/ezqt-app/api/reference/ui/)    | UI orchestration and reusable components | Theme, menus, panels, widgets   |

## Import Examples

Primary imports are exposed from the root package:

```python
from ezqt_app import EzApplication, EzQt_App, init
```

Service-level imports can be done from submodules:

```python
from ezqt_app.services.settings import get_settings_service
from ezqt_app.services.translation import get_translation_service
```

---

## Modules

| Module                                                                              | Scope                                | Notes                        |
| ----------------------------------------------------------------------------------- | ------------------------------------ | ---------------------------- |
| [Application Layer](https://neuraaak.github.io/ezqt-app/api/reference/application/) | Main window, bootstrap orchestration | Entrypoint and app shell     |
| [Config and Runtime](https://neuraaak.github.io/ezqt-app/api/reference/config/)     | Config/settings/runtime services     | Stateful infrastructure      |
| [Translation](https://neuraaak.github.io/ezqt-app/api/reference/translation/)       | Translation manager and providers    | Local TS + optional API      |
| [UI Services and Widgets](https://neuraaak.github.io/ezqt-app/api/reference/ui/)    | UI services and reusable widgets     | Presentation and interaction |

---

## Core Entry Points

- `ezqt_app.init(...)`
- `ezqt_app.EzApplication`
- `ezqt_app.EzQt_App`

---

## API Sections

- [Application Layer](https://neuraaak.github.io/ezqt-app/api/reference/application/)
- [Configuration and Runtime](https://neuraaak.github.io/ezqt-app/api/reference/config/)
- [Translation and Localization](https://neuraaak.github.io/ezqt-app/api/reference/translation/)
- [UI Services and Widgets](https://neuraaak.github.io/ezqt-app/api/reference/ui/)

---

## Source Tree

Main package: `src/ezqt_app/`

- `domain/`
- `services/`
- `widgets/`
- `utils/`
- `cli/`

---

## API Design Principles

### Type Safety

- Typed domain ports and models in `domain/`
- Service interfaces represented by protocols
- Static type checks configured in project tooling

```python
from ezqt_app.domain.ports.config_service import ConfigServiceProtocol
from ezqt_app.services.config.config_service import ConfigService

# ConfigService satisfies ConfigServiceProtocol at the boundary
service: ConfigServiceProtocol = ConfigService()
```

### Layered Boundaries

- `domain/` defines contracts
- `services/` implement adapters
- `widgets/` consume services and render UI

```python
# Services are accessed via helper functions, not instantiated directly
from ezqt_app.services.settings import get_settings_service
from ezqt_app.services.translation import get_translation_service

settings = get_settings_service()
translation = get_translation_service()
```

### Translation Behavior

- Widget registration and string collection are local workflow features
- `auto_translation_enabled` gates external provider calls

```python
from ezqt_app.services.translation import change_language_by_code

# Switch language at runtime
change_language_by_code("fr")

# Control auto-translation per window
window = EzQt_App()
window.enable_auto_translation(False)
```

---

## Quick Start Example

```python
import sys
from ezqt_app import EzApplication, EzQt_App, init

init()
app = EzApplication(sys.argv)
window = EzQt_App()
window.show()
sys.exit(app.exec())
```

---

## Installation

```bash
pip install ezqt-app
```

For development installation:

```bash
git clone https://github.com/neuraaak/ezqt-app.git
cd ezqt_app
pip install -e ".[dev]"
```

---

## Detailed Documentation

Select a module from the navigation menu or the table above to view detailed service documentation with:

- Complete method signatures
- Protocol/port definitions
- Initialization flows
- Usage examples

## Module Documentation

| Module                                                                              | Description                                          |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [Application Layer](https://neuraaak.github.io/ezqt-app/api/reference/application/) | Main window, bootstrap orchestration, app shell      |
| [Config and Runtime](https://neuraaak.github.io/ezqt-app/api/reference/config/)     | Config, settings, runtime state services             |
| [Translation](https://neuraaak.github.io/ezqt-app/api/reference/translation/)       | Translation manager, providers, string collection    |
| [UI Services and Widgets](https://neuraaak.github.io/ezqt-app/api/reference/ui/)    | UI orchestration, theme, menus, panels, core widgets |

---

## Need Help?

- [Getting Started](https://neuraaak.github.io/ezqt-app/getting-started/)
- [User Guides](https://neuraaak.github.io/ezqt-app/guides/)
- [CLI Reference](https://neuraaak.github.io/ezqt-app/cli/)
- [Issues](https://github.com/neuraaak/ezqt-app/issues)
