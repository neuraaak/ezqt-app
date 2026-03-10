# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION.MANAGER - Translation engine
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Core translation manager — QTranslator wrapper with widget retranslation support."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import sys
from pathlib import Path
from typing import Any

# Third-party imports
from PySide6.QtCore import QCoreApplication, QObject, QTranslator, Signal

# Local imports
from ...domain.models.translation import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from ...services.config import get_config_service
from ...utils.diagnostics import warn_tech, warn_user
from ...utils.printer import get_printer
from ...utils.runtime_paths import APP_PATH
from .auto_translator import get_auto_translator


# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////
def _parse_bool(raw: object) -> bool:
    """Parse a config value as bool, supporting string representations."""
    if isinstance(raw, str):
        return raw.strip().lower() in {"1", "true", "yes", "on"}
    return bool(raw)


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class TranslationManager(QObject):
    """Core translation engine for EzQt_App.

    Handles .ts file loading, language switching, Qt translator installation
    and automatic widget retranslation on language change.
    """

    languageChanged = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.translator = QTranslator()
        self.current_language = DEFAULT_LANGUAGE

        self._translatable_widgets: list[Any] = []
        self._translatable_texts: dict[Any, str] = {}
        self._ts_translations: dict[str, str] = {}

        self.auto_translator = get_auto_translator()
        self.auto_translation_enabled = False
        self.auto_save_translations = False

        try:
            translation_cfg = (
                get_config_service().load_config("translation").get("translation", {})
            )
            if isinstance(translation_cfg, dict):
                self.auto_translation_enabled = _parse_bool(
                    translation_cfg.get("auto_translation_enabled", False)
                )
                self.auto_save_translations = _parse_bool(
                    translation_cfg.get("save_to_ts_files", False)
                )
        except Exception as e:
            warn_tech(
                code="translation.manager.config_load_failed",
                message="Could not load translation config; using defaults (disabled)",
                error=e,
            )

        self.auto_translator.enabled = self.auto_translation_enabled

        # Resolve translations directory
        if hasattr(sys, "_MEIPASS"):
            self.translations_dir: Path | None = (
                Path(sys._MEIPASS) / "ezqt_app" / "resources" / "translations"
            )
        else:
            project_path = Path.cwd()
            possible_paths = [
                project_path / "bin" / "translations",
                APP_PATH / "bin" / "translations",
                Path(__file__).parent.parent.parent / "resources" / "translations",
            ]
            try:
                pkg_dir = self._get_package_translations_dir()
                if pkg_dir.exists():
                    possible_paths.append(pkg_dir)
            except Exception as e:
                warn_tech(
                    code="translation.manager.package_dir_resolution_failed",
                    message="Could not resolve package translations dir",
                    error=e,
                )

            self.translations_dir = next(
                (p for p in possible_paths if p.exists()), None
            )
            if self.translations_dir is None:
                self.translations_dir = project_path / "bin" / "translations"
                self.translations_dir.mkdir(parents=True, exist_ok=True)

        self.language_mapping: dict[str, str] = {
            "English": "en",
            "Français": "fr",
            "Español": "es",
            "Deutsch": "de",
        }

    def _get_package_translations_dir(self) -> Path:
        try:
            import pkg_resources  # type: ignore[import-untyped]

            return Path(
                pkg_resources.resource_filename("ezqt_app", "resources/translations")
            )
        except Exception:
            return Path(__file__).parent.parent.parent / "resources" / "translations"

    def _load_ts_file(self, ts_file_path: Path) -> bool:
        try:
            import xml.etree.ElementTree as ET

            if not ts_file_path.exists():
                return False

            root = ET.parse(ts_file_path).getroot()  # noqa: S314
            translations: dict[str, str] = {}
            for message in root.findall(".//message"):
                source = message.find("source")
                translation = message.find("translation")
                if (
                    source is not None
                    and translation is not None
                    and source.text
                    and translation.text
                ):
                    translations[source.text] = translation.text

            self._ts_translations.update(translations)
            return True
        except Exception as e:
            warn_tech(
                code="translation.manager.load_ts_failed",
                message=f"Error loading .ts file {ts_file_path}",
                error=e,
            )
            return False

    def load_language(self, language_name: str) -> bool:
        name_to_code = {
            info["name"]: code for code, info in SUPPORTED_LANGUAGES.items()
        }
        if language_name in name_to_code:
            return self.load_language_by_code(name_to_code[language_name])
        return False

    def load_language_by_code(self, language_code: str) -> bool:
        if language_code not in SUPPORTED_LANGUAGES:
            warn_user(
                code="translation.manager.unsupported_language",
                user_message=f"Unsupported language: {language_code}",
            )
            return False

        app = QCoreApplication.instance()
        if app is not None:
            try:
                QCoreApplication.removeTranslator(self.translator)
            except Exception as e:
                warn_tech(
                    code="translation.manager.remove_translator_failed",
                    message="Error removing translator",
                    error=e,
                )

        self.translator = QTranslator()
        language_info = SUPPORTED_LANGUAGES[language_code]

        if self.translations_dir is None:
            warn_tech(
                code="translation.manager.translations_dir_unavailable",
                message=(
                    "Translations directory not resolved; .ts file load skipped "
                    f"for language '{language_code}'"
                ),
            )
            self._retranslate_all_widgets()
            self.languageChanged.emit(language_code)
            return True

        ts_file_path = self.translations_dir / language_info["file"]

        if self._load_ts_file(ts_file_path):
            if app is not None:
                try:
                    QCoreApplication.installTranslator(self.translator)
                except Exception as e:
                    warn_tech(
                        code="translation.manager.install_translator_failed",
                        message="Error installing translator",
                        error=e,
                    )
            self.current_language = language_code
            get_printer().info(f"Language switched to {language_info['name']}")
        else:
            warn_user(
                code="translation.manager.load_language_failed",
                user_message=(
                    f"Unable to load translations for {language_info['name']}"
                ),
            )

        self._retranslate_all_widgets()
        self.languageChanged.emit(language_code)
        return True

    def get_available_languages(self) -> list[str]:
        return list(SUPPORTED_LANGUAGES.keys())

    def get_current_language_name(self) -> str:
        if self.current_language in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[self.current_language]["name"]
        return "Unknown"

    def get_current_language_code(self) -> str:
        return self.current_language

    def translate(self, text: str) -> str:
        if text in self._ts_translations:
            return self._ts_translations[text]

        translated = self.translator.translate("", text)
        if translated and translated != text:
            return translated

        if self.auto_translation_enabled and self.auto_translator.enabled:
            auto_translated = self.auto_translator.translate_sync(
                text, "en", self.current_language
            )
            if auto_translated:
                if self.auto_save_translations:
                    self._save_auto_translation_to_ts(text, auto_translated)
                return auto_translated

        return text

    def register_widget(self, widget: Any, original_text: str) -> None:
        if widget not in self._translatable_widgets:
            self._translatable_widgets.append(widget)
            self._translatable_texts[widget] = original_text

    def unregister_widget(self, widget: Any) -> None:
        if widget in self._translatable_widgets:
            self._translatable_widgets.remove(widget)
            self._translatable_texts.pop(widget, None)

    def set_translatable_text(self, widget: Any, text: str) -> None:
        self.register_widget(widget, text)
        self._set_widget_text(widget, text)

    def _set_widget_text(self, widget: Any, text: str) -> None:
        try:
            translated = self.translate(text)
            if hasattr(widget, "setText"):
                widget.setText(translated)
            elif hasattr(widget, "setTitle"):
                widget.setTitle(translated)
            elif hasattr(widget, "setWindowTitle"):
                widget.setWindowTitle(translated)
            elif hasattr(widget, "setPlaceholderText"):
                widget.setPlaceholderText(translated)
            elif hasattr(widget, "setToolTip"):
                widget.setToolTip(translated)
            else:
                warn_tech(
                    code="translation.manager.unsupported_widget_for_translation",
                    message=f"Widget type not supported for translation: {type(widget)}",
                )
        except Exception as e:
            warn_tech(
                code="translation.manager.widget_translation_failed",
                message="Error translating widget",
                error=e,
            )

    def _retranslate_all_widgets(self) -> None:
        for widget in self._translatable_widgets:
            if widget in self._translatable_texts:
                self._set_widget_text(widget, self._translatable_texts[widget])

    def clear_registered_widgets(self) -> None:
        self._translatable_widgets.clear()
        self._translatable_texts.clear()

    def _save_auto_translation_to_ts(self, original: str, translated: str) -> None:
        try:
            if self.current_language in SUPPORTED_LANGUAGES:
                if self.translations_dir is None:
                    return
                language_info = SUPPORTED_LANGUAGES[self.current_language]
                ts_file_path = self.translations_dir / language_info["file"]
                self.auto_translator.save_translation_to_ts(
                    original, translated, self.current_language, ts_file_path
                )
                self._ts_translations[original] = translated
        except Exception as e:
            warn_tech(
                code="translation.manager.auto_translation_save_failed",
                message="Error saving automatic translation",
                error=e,
            )

    def enable_auto_translation(self, enabled: bool = True) -> None:
        self.auto_translation_enabled = enabled
        if self.auto_translator:
            self.auto_translator.enabled = enabled
        get_printer().info(
            f"Automatic translation {'enabled' if enabled else 'disabled'}"
        )

    def get_auto_translation_stats(self) -> dict[str, Any]:
        if self.auto_translator:
            return self.auto_translator.get_cache_stats()
        return {}

    def clear_auto_translation_cache(self) -> None:
        if self.auto_translator:
            self.auto_translator.clear_cache()


# ///////////////////////////////////////////////////////////////
# SINGLETON
# ///////////////////////////////////////////////////////////////
_translation_manager_instance: TranslationManager | None = None


def get_translation_manager() -> TranslationManager:
    """Return the global TranslationManager singleton."""
    global _translation_manager_instance, translation_manager
    if _translation_manager_instance is None:
        _translation_manager_instance = TranslationManager()
        translation_manager = _translation_manager_instance
    return _translation_manager_instance


translation_manager: TranslationManager | None = None
