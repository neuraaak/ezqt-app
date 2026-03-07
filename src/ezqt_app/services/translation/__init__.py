# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION - Translation services
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Translation services — manager, helpers, auto-translator, string collector."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
from ...domain.models.translation import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from .helpers import (
    change_language,
    clear_auto_translation_cache,
    collect_and_compare_strings,
    collect_strings_from_widget,
    enable_auto_translation,
    get_auto_translation_stats,
    get_available_languages,
    get_current_language,
    get_new_strings,
    get_string_collector_stats,
    get_translation_stats,
    mark_strings_as_processed,
    mark_strings_as_registered,
    register_tr,
    register_widgets_manually,
    scan_and_register_widgets,
    scan_widgets_for_translation,
    set_tr,
    tr,
    translate_auto,
    unregister_tr,
)
from .manager import TranslationManager, get_translation_manager, translation_manager
from .translation_service import TranslationService, get_translation_service

# ///////////////////////////////////////////////////////////////
# VARIABLES
# ///////////////////////////////////////////////////////////////
TRANSLATIONS_DIR: str = "resources/translations"

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    # Config
    "SUPPORTED_LANGUAGES",
    "DEFAULT_LANGUAGE",
    "TRANSLATIONS_DIR",
    # Manager
    "TranslationManager",
    "get_translation_manager",
    "translation_manager",
    # Service (Port adapter)
    "TranslationService",
    "get_translation_service",
    # Helpers
    "tr",
    "set_tr",
    "register_tr",
    "unregister_tr",
    "change_language",
    "get_available_languages",
    "get_current_language",
    "enable_auto_translation",
    "get_auto_translation_stats",
    "clear_auto_translation_cache",
    "translate_auto",
    "scan_widgets_for_translation",
    "register_widgets_manually",
    "scan_and_register_widgets",
    "get_translation_stats",
    "collect_strings_from_widget",
    "collect_and_compare_strings",
    "get_new_strings",
    "mark_strings_as_processed",
    "mark_strings_as_registered",
    "get_string_collector_stats",
]
