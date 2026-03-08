# Translation and Localization

Translation stack: service adapter, manager, auto-translation providers, and string collection.

---

## TranslationService

::: ezqt_app.services.translation.translation_service.TranslationService

---

## TranslationManager

::: ezqt_app.services.translation.manager.TranslationManager

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
Widget registration and string collection are local workflow features and can remain enabled independently.
