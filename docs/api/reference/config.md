# Configuration and runtime

Configuration and runtime state services for project setup and UI behavior.

## ⚠️ Strict validation contracts

`ConfigService.save_config()` now validates known payloads in strict mode
before writing files:

| Config file               | Validated sections                                         |
| :------------------------ | :--------------------------------------------------------- |
| `app.config.yaml`         | `app`, `settings_panel`                                    |
| `translation.config.yaml` | `translation`, `language_detection`, `supported_languages` |
| `theme.config.yaml`       | `palette`                                                  |

Unknown keys in validated sections are rejected (strict schema mode).
When validation fails, the file is not written.

## 🎨 Theme default source

The default/active theme is read from `settings_panel.theme.default` in
`app.config.yaml`.

`app.theme` is no longer part of the configuration contract.

## 📦 ConfigService

::: ezqt_app.services.config.config_service.ConfigService

## 📦 SettingsService

::: ezqt_app.services.settings.settings_service.SettingsService

## 📦 RuntimeStateService

::: ezqt_app.services.runtime.runtime_service.RuntimeStateService

## 🔍 Related ports

- `ezqt_app.domain.ports.config_service.ConfigServiceProtocol`
- `ezqt_app.domain.ports.settings_service.SettingsServiceProtocol`
- `ezqt_app.domain.ports.runtime_state_service.RuntimeStateServiceProtocol`
