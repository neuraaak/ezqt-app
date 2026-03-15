# ///////////////////////////////////////////////////////////////
# DOMAIN.PORTS.MAIN_WINDOW - Main window structural contract
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Structural Protocol for the main application window.

UI services interact with the main window through this contract instead of
``Any``.  This makes all required attributes explicit and enables static
analysis without coupling the domain layer to PySide6 at runtime (all Qt
imports are guarded by ``TYPE_CHECKING``).

Sub-protocols model the ``window.ui.*`` sub-objects accessed by UI services.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from PySide6.QtCore import QPoint, QPropertyAnimation, QSize, Qt
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QGraphicsDropShadowEffect, QSizeGrip, QToolButton


# ///////////////////////////////////////////////////////////////
# SUB-PROTOCOLS — window.ui.*
# ///////////////////////////////////////////////////////////////
class StyleSheetWidgetProtocol(Protocol):
    """Minimal contract for the style-sheet target widget (``ui.styleSheet``)."""

    def setStyleSheet(self, style: str) -> None: ...


class AppMarginsProtocol(Protocol):
    """Minimal contract for the outer margin container (``ui.appMargins``)."""

    def setContentsMargins(
        self, left: int, top: int, right: int, bottom: int
    ) -> None: ...


class _AppButtonProtocol(Protocol):
    """Minimal contract for a single header action button."""

    clicked: Any  # PySide6 Signal — typed as Any to stay Qt-agnostic

    def hide(self) -> None: ...
    def setToolTip(self, tip: str) -> None: ...
    def setIcon(self, icon: QIcon) -> None: ...


class HeaderContainerProtocol(Protocol):
    """Minimal contract for the title-bar / header widget (``ui.headerContainer``)."""

    minimizeAppBtn: _AppButtonProtocol
    maximizeRestoreAppBtn: _AppButtonProtocol
    closeAppBtn: _AppButtonProtocol
    mouseDoubleClickEvent: Any  # settable event handler
    mouseMoveEvent: Any  # settable event handler

    def set_app_name(self, name: str) -> None: ...
    def set_app_description(self, description: str) -> None: ...


class _SizeGripSlotProtocol(Protocol):
    """Minimal contract for the size-grip placeholder in the bottom bar."""

    def hide(self) -> None: ...
    def show(self) -> None: ...


class BottomBarProtocol(Protocol):
    """Minimal contract for the bottom status / size-grip bar (``ui.bottomBar``)."""

    appSizeGrip: _SizeGripSlotProtocol


class _TopMenuProtocol(Protocol):
    """Minimal contract for the top-menu widget (``ui.menuContainer.topMenu``)."""

    def findChildren(self, child_type: type[QToolButton]) -> list[QToolButton]: ...


class MenuContainerProtocol(Protocol):
    """Minimal contract for the collapsible left menu (``ui.menuContainer``)."""

    topMenu: _TopMenuProtocol

    def width(self) -> int: ...
    def get_extended_width(self) -> int: ...
    def get_shrink_width(self) -> int: ...


class SettingsPanelProtocol(Protocol):
    """Minimal contract for the settings slide-in panel (``ui.settingsPanel``)."""

    def width(self) -> int: ...
    def get_theme_toggle_button(self) -> Any: ...


class BgAppProtocol(Protocol):
    """Minimal contract for the background app widget (``ui.bgApp``)."""

    def setGraphicsEffect(self, effect: QGraphicsDropShadowEffect) -> None: ...


class MainUiProtocol(Protocol):
    """Aggregated contract for the ``window.ui`` object."""

    styleSheet: StyleSheetWidgetProtocol
    appMargins: AppMarginsProtocol
    headerContainer: HeaderContainerProtocol
    bottomBar: BottomBarProtocol
    menuContainer: MenuContainerProtocol
    settingsPanel: SettingsPanelProtocol
    bgApp: BgAppProtocol


# ///////////////////////////////////////////////////////////////
# SUB-PROTOCOL — window grips
# ///////////////////////////////////////////////////////////////
class GripProtocol(Protocol):
    """Minimal contract for a custom resize grip handle."""

    def hide(self) -> None: ...
    def show(self) -> None: ...
    def setGeometry(self, x: int, y: int, w: int, h: int) -> None: ...


# ///////////////////////////////////////////////////////////////
# MAIN PROTOCOL
# ///////////////////////////////////////////////////////////////
class MainWindowProtocol(Protocol):
    """Structural contract expected by UI services from the main application window.

    Services use this type instead of ``Any`` for their *window* parameters,
    making all accessed attributes explicit and verifiable by static analysis.

    Attributes that are *written* by services (grips, shadow, animations…) are
    included because other services read them later; their presence is guaranteed
    by the call ordering in the boot sequence.
    """

    # ── UI sub-object ──────────────────────────────────────────
    ui: MainUiProtocol

    # ── Custom resize grips (set + read by services) ───────────
    left_grip: GripProtocol
    right_grip: GripProtocol
    top_grip: GripProtocol
    bottom_grip: GripProtocol

    # ── Dynamic state attributes (set by services) ─────────────
    dragPos: QPoint
    shadow: QGraphicsDropShadowEffect
    sizegrip: QSizeGrip
    menu_animation: QPropertyAnimation
    settings_animation: QPropertyAnimation

    # ── Standard QWidget / QMainWindow methods ─────────────────
    def showMaximized(self) -> None: ...
    def showNormal(self) -> None: ...
    def showMinimized(self) -> None: ...
    def close(self) -> bool: ...
    def resize(self, w: int, h: int) -> None: ...
    def move(self, pos: QPoint) -> None: ...
    def pos(self) -> QPoint: ...
    def width(self) -> int: ...
    def height(self) -> int: ...
    def setMinimumSize(self, size: QSize) -> None: ...
    def setWindowFlags(self, flags: Qt.WindowType) -> None: ...
    def setAttribute(self, attribute: Qt.WidgetAttribute) -> None: ...
