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
from ...utils.diagnostics import warn_tech
from .manager import get_translation_manager


# ///////////////////////////////////////////////////////////////
# TRANSLATION HELPERS
# ///////////////////////////////////////////////////////////////
def tr(text: str) -> str:
    """Translate *text* using the active language context."""
    return get_translation_manager().translate(text)


def set_tr(widget: Any, text: str) -> None:
    """Set translated text on *widget* and register it for auto-retranslation."""
    get_translation_manager().set_translatable_text(widget, text)


def register_tr(widget: Any, text: str) -> None:
    """Register *widget* for auto-retranslation without changing its text immediately."""
    get_translation_manager().register_widget(widget, text)


def unregister_tr(widget: Any) -> None:
    """Unregister *widget* from auto-retranslation."""
    get_translation_manager().unregister_widget(widget)


def change_language(language_name: str) -> bool:
    """Switch the application language by display name (e.g. ``"Français"``)."""
    return get_translation_manager().load_language(language_name)


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


def translate_auto(
    text: str, source_lang: str = "en", target_lang: str | None = None
) -> str:
    """Translate *text* via an external provider (requires auto-translation enabled)."""
    manager = get_translation_manager()
    if target_lang is None:
        target_lang = manager.get_current_language_code()

    if manager.auto_translation_enabled and manager.auto_translator.enabled:
        translated = manager.auto_translator.translate_sync(
            text, source_lang, target_lang
        )
        if translated:
            return translated

    return text


# ///////////////////////////////////////////////////////////////
# WIDGET SCANNING HELPERS
# ///////////////////////////////////////////////////////////////
def scan_widgets_for_translation(
    widget: Any, recursive: bool = True
) -> list[tuple[Any, str]]:
    """Scan *widget* (and optionally children) for translatable text."""
    from PySide6.QtWidgets import QWidget

    found: list[tuple[Any, str]] = []

    def scan_recursive(w: Any) -> None:
        try:
            if hasattr(w, "text") and callable(getattr(w, "text", None)):
                try:
                    text = w.text().strip()
                    if (
                        text
                        and not text.isdigit()
                        and len(text) > 1
                        and not text.startswith(("_", "menu_", "btn_", "setting"))
                    ):
                        found.append((w, text))
                except Exception as e:
                    warn_tech(
                        code="translation.helpers.scan.read_text_failed",
                        message="Could not read widget text",
                        error=e,
                    )

            if hasattr(w, "toolTip") and callable(getattr(w, "toolTip", None)):
                try:
                    tooltip = w.toolTip().strip()
                    if (
                        tooltip
                        and not tooltip.isdigit()
                        and len(tooltip) > 1
                        and not tooltip.startswith("_")
                    ):
                        found.append((w, tooltip))
                except Exception as e:
                    warn_tech(
                        code="translation.helpers.scan.read_tooltip_failed",
                        message="Could not read widget toolTip",
                        error=e,
                    )

            if hasattr(w, "placeholderText") and callable(
                getattr(w, "placeholderText", None)
            ):
                try:
                    placeholder = w.placeholderText().strip()
                    if (
                        placeholder
                        and not placeholder.isdigit()
                        and len(placeholder) > 1
                        and not placeholder.startswith("_")
                    ):
                        found.append((w, placeholder))
                except Exception as e:
                    warn_tech(
                        code="translation.helpers.scan.read_placeholder_failed",
                        message="Could not read widget placeholderText",
                        error=e,
                    )

            if recursive:
                try:
                    for child in w.findChildren(QWidget):
                        scan_recursive(child)
                except Exception as e:
                    warn_tech(
                        code="translation.helpers.scan.iter_children_failed",
                        message="Could not iterate widget children",
                        error=e,
                    )

        except Exception as e:
            warn_tech(
                code="translation.helpers.scan.widget_failed",
                message=f"Error scanning widget {type(w)}",
                error=e,
            )

    scan_recursive(widget)
    return found


def register_widgets_manually(widgets_list: list[tuple[Any, str]]) -> int:
    """Register a list of ``(widget, text)`` tuples for translation.

    Returns the number of successfully registered widgets.
    """
    count = 0
    for widget, text in widgets_list:
        try:
            register_tr(widget, text)
            count += 1
        except Exception as e:
            warn_tech(
                code="translation.helpers.register_widget_failed",
                message="Error registering widget",
                error=e,
            )
    return count


def scan_and_register_widgets(widget: Any, recursive: bool = True) -> int:
    """Scan *widget* and register all found translatable widgets.

    Returns the number of registered widgets.
    """
    return register_widgets_manually(scan_widgets_for_translation(widget, recursive))


# ///////////////////////////////////////////////////////////////
# STATS HELPERS
# ///////////////////////////////////////////////////////////////
def get_translation_stats() -> dict[str, Any]:
    """Return complete translation system statistics."""
    manager = get_translation_manager()
    return {
        "registered_widgets": len(manager._translatable_widgets),
        "cached_translations": len(manager._ts_translations),
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


def mark_strings_as_registered(strings: set[str] | None = None) -> None:
    """Alias for :func:`mark_strings_as_processed` (backward compat)."""
    mark_strings_as_processed(strings)


def get_string_collector_stats() -> dict[str, Any]:
    """Return string collector statistics."""
    from .string_collector import get_string_collector

    return get_string_collector().get_stats()
