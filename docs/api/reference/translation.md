# Translation and Localization

Translation stack: service adapter, manager, auto-translation providers, and string collection.

---

## TranslationService

::: ezqt_app.services.translation.translation_service.TranslationService

---

## TranslationManager

::: ezqt_app.services.translation.manager.TranslationManager

---

## EzTranslator

`EzTranslator` is a `QTranslator` subclass installed permanently into Qt's translator chain. It intercepts every `QCoreApplication.translate("EzQt_App", text)` call made by any widget:

- **Cache hit** — returns the translation immediately from the in-memory `_ts_translations` dictionary.
- **Identity** — when the current language equals the source language (`en` by default), returns `source_text` as-is and persists the identity mapping to the source `.ts` file.
- **Cache miss** — dispatches an async translation request (daemon thread) via `AutoTranslator` and returns `None` so Qt falls back to the source text for the current render cycle. When the translation arrives, `LanguageChange` is re-emitted and widgets retranslate automatically.

`EzTranslator` is installed once at `TranslationManager` init and is never removed, even during language switches (only the `.qm`-backed translator is swapped).

::: ezqt_app.services.translation.manager.EzTranslator

---

## AutoTranslator

::: ezqt_app.services.translation.auto_translator.AutoTranslator

---

## StringCollector

::: ezqt_app.services.translation.string_collector.StringCollector

---

## Providers

- `GoogleTranslateProvider`
- `MyMemoryProvider`
- `LibreTranslateProvider`

`auto_translation_enabled` in `translation.config.yaml` controls external provider calls.
`save_to_ts_files: true` enables runtime persistence: every translated string is appended to the active `.ts` file and the `.qm` is recompiled via `pyside6-lrelease`.
Widget registration and string collection are local workflow features and can remain enabled independently.
