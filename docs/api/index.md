# API reference

Complete API reference for **EzQt App**, organized by architectural responsibility.

## 📦 Modules

| Module                                        | Description                                                            |
| :-------------------------------------------- | :--------------------------------------------------------------------- |
| [Asset catalog](assets.md)                    | Exhaustive list of embedded icons/images and runtime asset accessors   |
| [Application layer](reference/application.md) | Main window shell, bootstrap entrypoints, initialization sequence      |
| [Config and runtime](reference/config.md)     | Configuration load/save, mutable settings state, runtime state service |
| [Translation](reference/translation.md)       | Translation manager, auto-translation providers, string collection     |
| [UI services and widgets](reference/ui.md)    | Theme, menu, panel, window services and reusable widget containers     |

## 🔍 Core entry points

```python
from ezqt_app import EzApplication, EzQt_App, init
```

Service-level imports:

```python
from ezqt_app.services.settings import get_settings_service
from ezqt_app.services.translation import get_translation_service
```

Protocol imports:

```python
from ezqt_app.domain.ports.config_service import ConfigServiceProtocol
from ezqt_app.domain.ports.settings_service import SettingsServiceProtocol
from ezqt_app.domain.ports.runtime_state_service import RuntimeStateServiceProtocol
```

## 📁 Source tree

```text
src/ezqt_app/
├── domain/     # contracts (protocols) and domain models
├── services/   # adapters and orchestration
├── widgets/    # presentation layer
├── utils/
└── cli/
```
