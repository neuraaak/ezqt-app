# Translation and localization

Translation stack: service adapter, manager, auto-translation providers, and string collection.

## 📦 TranslationService

::: ezqt_app.services.translation.translation_service.TranslationService

## 📦 TranslationManager

::: ezqt_app.services.translation.manager.TranslationManager

## 📡 Translation signal integration

`TranslationManager` exposes runtime signals used by the UI layer:

| Signal                 | Payload               | Purpose                                                  |
| :--------------------- | :-------------------- | :------------------------------------------------------- |
| `languageChanged`      | `str` (language code) | Notify widgets/services that the active language changed |
| `translation_started`  | none                  | Notify that async auto-translation queue became active   |
| `translation_finished` | none                  | Notify that async auto-translation queue drained         |

`AutoTranslator` also emits low-level worker signals:

| Signal              | Payload                  | Purpose                                      |
| :------------------ | :----------------------- | :------------------------------------------- |
| `translation_ready` | `(original, translated)` | One async translation completed successfully |
| `translation_error` | `(original, error)`      | One async translation failed                 |

Example wiring:

```python
from ezqt_app.services.translation import get_translation_manager

manager = get_translation_manager()

manager.languageChanged.connect(lambda code: print(f"Language -> {code}"))
manager.translation_started.connect(lambda: print("Auto-translation started"))
manager.translation_finished.connect(lambda: print("Auto-translation finished"))
```

## 📦 EzTranslator

`EzTranslator` is a `QTranslator` subclass installed permanently into Qt's translator
chain. It intercepts every `QCoreApplication.translate("EzQt_App", text)` call made
by any widget:

- **Cache hit** — returns the translation immediately from the in-memory `_ts_translations` dictionary.
- **Identity** — when the current language equals the source language (`en` by default), returns `source_text` as-is and persists the identity mapping to the source `.ts` file.
- **Cache miss** — dispatches an async translation request (daemon thread) via `AutoTranslator` and returns `None` so Qt falls back to the source text for the current render cycle. When the translation arrives, `LanguageChange` is re-emitted and widgets retranslate automatically.

`EzTranslator` is installed once at `TranslationManager` init and is never removed,
even during language switches (only the `.qm`-backed translator is swapped).

::: ezqt_app.services.translation.manager.EzTranslator

## 📦 AutoTranslator

::: ezqt_app.services.translation.auto_translator.AutoTranslator

## ⚠️ Provider response validation

External HTTP payloads from providers are schema-validated before use.

| Provider                  | Validation mode             |
| :------------------------ | :-------------------------- |
| `GoogleTranslateProvider` | strict payload shape checks |
| `MyMemoryProvider`        | strict object schema checks |
| `LibreTranslateProvider`  | strict object schema checks |

Invalid payloads are rejected and logged; translation returns `None`.

## ⚠️ Cache contract

`translations.json` is validated with a strict schema on read and write.
Malformed entries are removed or rejected instead of being tolerated.

## ⚠️ Legacy fallback removed

`LibreTranslateProvider` no longer auto-falls back to an alternate host when
the primary host returns an HTTP error.

## 📦 StringCollector

::: ezqt_app.services.translation.string_collector.StringCollector

## 🔍 Providers

Available provider implementations:

- `GoogleTranslateProvider`
- `MyMemoryProvider`
- `LibreTranslateProvider`

`auto_translation_enabled` in `translation.config.yaml` controls external provider calls.
`save_to_ts_files: true` enables runtime persistence: every translated string is appended
to the active `.ts` file and the `.qm` is recompiled via `pyside6-lrelease`.
Widget registration and string collection are local workflow features and can remain
enabled independently.
