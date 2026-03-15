# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION.HELPERS - Translation convenience functions
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Thin helper functions over TranslationManager for ergonomic API access."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Any

# Local imports
from .manager import get_translation_manager


# ///////////////////////////////////////////////////////////////
# TRANSLATION HELPERS
# ///////////////////////////////////////////////////////////////
def tr(text: str) -> str:
    """Translate *text* using the active language context."""
    return get_translation_manager().translate(text)


def change_language(language_name: str) -> bool:
    """Switch the application language by display name (e.g. ``"Français"``)."""
    return get_translation_manager().load_language(language_name)


def change_language_by_code(language_code: str) -> bool:
    """Switch the application language by ISO code (e.g. ``"fr"``)."""
    return get_translation_manager().load_language_by_code(language_code)


def get_available_languages() -> list[str]:
    """Return list of available language codes."""
    return get_translation_manager().get_available_languages()


def get_current_language() -> str:
    """Return the current language display name."""
    return get_translation_manager().get_current_language_name()


def enable_auto_translation(enabled: bool = True) -> None:
    """Enable or disable automatic translation."""
    get_translation_manager().enable_auto_translation(enabled)


def get_auto_translation_stats() -> dict[str, Any]:
    """Return automatic translation cache statistics."""
    return get_translation_manager().get_auto_translation_stats()


def clear_auto_translation_cache() -> None:
    """Clear the automatic translation cache."""
    get_translation_manager().clear_auto_translation_cache()


# ///////////////////////////////////////////////////////////////
# STATS HELPERS
# ///////////////////////////////////////////////////////////////
def get_translation_stats() -> dict[str, Any]:
    """Return complete translation system statistics."""
    manager = get_translation_manager()
    return {
        "cached_translations": manager.translation_count,
        "current_language": manager.get_current_language_name(),
        "available_languages": manager.get_available_languages(),
        "auto_translation_enabled": manager.auto_translation_enabled,
        "auto_translation_stats": manager.get_auto_translation_stats(),
    }


# ///////////////////////////////////////////////////////////////
# STRING COLLECTOR HELPERS
# ///////////////////////////////////////////////////////////////
def collect_strings_from_widget(widget: Any, recursive: bool = True) -> set[str]:
    """Collect all UI strings from *widget* (for translation workflow)."""
    from .string_collector import get_string_collector

    return get_string_collector().collect_strings_from_widget(widget, recursive)


def collect_and_compare_strings(widget: Any, recursive: bool = True) -> dict[str, Any]:
    """Collect strings and compare with already-processed ones."""
    from .string_collector import get_string_collector

    return get_string_collector().collect_and_compare(widget, recursive)


def get_new_strings() -> set[str]:
    """Return strings collected but not yet marked as processed."""
    from .string_collector import get_string_collector

    return get_string_collector().get_new_strings()


def mark_strings_as_processed(strings: set[str] | None = None) -> None:
    """Mark *strings* as processed (default: all new strings)."""
    from .string_collector import get_string_collector

    get_string_collector().mark_strings_as_processed(strings)


def get_string_collector_stats() -> dict[str, Any]:
    """Return string collector statistics."""
    from .string_collector import get_string_collector

    return get_string_collector().get_stats()
