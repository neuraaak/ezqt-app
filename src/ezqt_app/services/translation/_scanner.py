# ///////////////////////////////////////////////////////////////
# SERVICES.TRANSLATION._SCANNER - Unified widget text scanner
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unified widget scanner for translatable text discovery."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

# Local imports
from ...utils.diagnostics import warn_tech


# ///////////////////////////////////////////////////////////////
# TYPES
# ///////////////////////////////////////////////////////////////
class TextRole(StrEnum):
    """Semantic role of a translatable text property.

    The enum value is the Qt setter method name (e.g. ``"setText"``),
    used by :func:`scan_widget` to detect which text attribute a widget exposes.
    """

    TEXT = "setText"
    TITLE = "setTitle"
    WINDOW_TITLE = "setWindowTitle"
    PLACEHOLDER = "setPlaceholderText"
    TOOLTIP = "setToolTip"


@dataclass(slots=True)
class WidgetEntry:
    """Binds a widget's stored original text to its semantic setter role."""

    original_text: str
    role: TextRole


# ///////////////////////////////////////////////////////////////
# FILTER
# ///////////////////////////////////////////////////////////////
_TECHNICAL_PREFIXES: tuple[str, ...] = ("_", "menu_", "btn_", "setting")

_TECHNICAL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^[A-Z_]+$"),  # CONST_NAMES
    re.compile(r"^[a-z_]+$"),  # snake_case
    re.compile(r"^[a-z]+[A-Z][a-z]+$"),  # camelCase
    re.compile(r"^[A-Z][a-z]+[A-Z][a-z]+$"),  # PascalCase
)


def is_translatable(text: str) -> bool:
    """Return ``True`` if *text* looks like a human-readable UI string."""
    if not text or len(text) < 2:
        return False
    if text.isdigit():
        return False
    if text.startswith(_TECHNICAL_PREFIXES):
        return False
    return not any(p.match(text) for p in _TECHNICAL_PATTERNS)


# ///////////////////////////////////////////////////////////////
# SCANNER
# ///////////////////////////////////////////////////////////////
def scan_widget(
    root: Any,
    *,
    include_tooltips: bool = True,
    include_placeholders: bool = True,
    recursive: bool = True,
) -> list[tuple[Any, WidgetEntry]]:
    """Scan *root* and return all translatable ``(widget, WidgetEntry)`` pairs.

    Uses ``FindDirectChildrenOnly`` for O(n) DFS — avoids the O(n²) revisiting
    caused by the default recursive ``findChildren``.
    Each widget is visited exactly once (tracked by ``id``).
    A widget may yield multiple entries (e.g. TEXT + TOOLTIP).
    """
    results: list[tuple[Any, WidgetEntry]] = []
    seen: set[int] = set()

    def _scan(w: Any) -> None:
        wid = id(w)
        if wid in seen:
            return
        seen.add(wid)

        try:
            if hasattr(w, "text") and callable(getattr(w, "text", None)):
                try:
                    text = w.text().strip()
                    if is_translatable(text):
                        results.append(
                            (w, WidgetEntry(original_text=text, role=TextRole.TEXT))
                        )
                except Exception as e:
                    warn_tech(
                        code="translation.scanner.read_text_failed",
                        message="Could not read widget text",
                        error=e,
                    )

            if (
                include_tooltips
                and hasattr(w, "toolTip")
                and callable(getattr(w, "toolTip", None))
            ):
                try:
                    tooltip = w.toolTip().strip()
                    if is_translatable(tooltip):
                        results.append(
                            (
                                w,
                                WidgetEntry(
                                    original_text=tooltip, role=TextRole.TOOLTIP
                                ),
                            )
                        )
                except Exception as e:
                    warn_tech(
                        code="translation.scanner.read_tooltip_failed",
                        message="Could not read widget toolTip",
                        error=e,
                    )

            if (
                include_placeholders
                and hasattr(w, "placeholderText")
                and callable(getattr(w, "placeholderText", None))
            ):
                try:
                    placeholder = w.placeholderText().strip()
                    if is_translatable(placeholder):
                        results.append(
                            (
                                w,
                                WidgetEntry(
                                    original_text=placeholder, role=TextRole.PLACEHOLDER
                                ),
                            )
                        )
                except Exception as e:
                    warn_tech(
                        code="translation.scanner.read_placeholder_failed",
                        message="Could not read widget placeholderText",
                        error=e,
                    )

            if recursive:
                try:
                    for child in w.findChildren(
                        QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly
                    ):
                        _scan(child)
                except Exception as e:
                    warn_tech(
                        code="translation.scanner.iter_children_failed",
                        message="Could not iterate widget children",
                        error=e,
                    )

        except Exception as e:
            warn_tech(
                code="translation.scanner.widget_failed",
                message=f"Error scanning widget {type(w)}",
                error=e,
            )

    _scan(root)
    return results


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["TextRole", "WidgetEntry", "is_translatable", "scan_widget"]
