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
from ._scanner import TextRole as TextRole  # re-export
from ._scanner import is_translatable as is_translatable  # re-export
from .helpers import (
    change_language,
    change_language_by_code,
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
    tr,
)
from .manager import TranslationManager, get_translation_manager
from .translation_service import TranslationService, get_translation_service

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    # Scanner
    "TextRole",
    "is_translatable",
    # Config
    "SUPPORTED_LANGUAGES",
    "DEFAULT_LANGUAGE",
    # Manager
    "TranslationManager",
    "get_translation_manager",
    # Service (Port adapter)
    "TranslationService",
    "get_translation_service",
    # Helpers
    "tr",
    "change_language",
    "change_language_by_code",
    "get_available_languages",
    "get_current_language",
    "enable_auto_translation",
    "get_auto_translation_stats",
    "clear_auto_translation_cache",
    "get_translation_stats",
    "collect_strings_from_widget",
    "collect_and_compare_strings",
    "get_new_strings",
    "mark_strings_as_processed",
    "get_string_collector_stats",
]
