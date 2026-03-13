"""
UI definitions service implementation.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from typing import Any

# Third-party imports
from PySide6.QtCore import QEvent, QSize, Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QSizeGrip

# Local imports
from ...utils.custom_grips import CustomGrip
from ..settings import get_settings_service
from .window_service import WindowService


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class UiDefinitionsService:
    """Service responsible for main window UI setup and grip resizing."""

    @staticmethod
    def apply_definitions(window: Any) -> None:
        """Configure all UI elements and connect base window events."""
        settings_service = get_settings_service()
        app_settings = settings_service.app

        def double_click_maximize_restore(event: Any) -> None:
            if event.type() == QEvent.Type.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: WindowService.maximize_restore(window))

        window.ui.headerContainer.mouseDoubleClickEvent = double_click_maximize_restore

        if app_settings.NAME:
            window.ui.headerContainer.set_app_name(app_settings.NAME)
        if app_settings.DESCRIPTION:
            window.ui.headerContainer.set_app_description(app_settings.DESCRIPTION)
        if app_settings.APP_WIDTH and app_settings.APP_HEIGHT:
            window.resize(app_settings.APP_WIDTH, app_settings.APP_HEIGHT)
        if app_settings.APP_MIN_SIZE:
            window.setMinimumSize(QSize(*app_settings.APP_MIN_SIZE))

        if app_settings.ENABLE_CUSTOM_TITLE_BAR:
            window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            def move_window(event: Any) -> None:
                if WindowService.get_status():
                    WindowService.maximize_restore(window)
                if event.buttons() == Qt.MouseButton.LeftButton:
                    window.move(window.pos() + event.globalPos() - window.dragPos)
                    window.dragPos = event.globalPos()
                    event.accept()

            window.ui.headerContainer.mouseMoveEvent = move_window

            window.left_grip = CustomGrip(window, Qt.Edge.LeftEdge, True)
            window.right_grip = CustomGrip(window, Qt.Edge.RightEdge, True)
            window.top_grip = CustomGrip(window, Qt.Edge.TopEdge, True)
            window.bottom_grip = CustomGrip(window, Qt.Edge.BottomEdge, True)
        else:
            window.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            window.ui.headerContainer.minimizeAppBtn.hide()
            window.ui.headerContainer.maximizeRestoreAppBtn.hide()
            window.ui.headerContainer.closeAppBtn.hide()
            window.ui.bottomBar.appSizeGrip.hide()

        window.shadow = QGraphicsDropShadowEffect(window)
        window.shadow.setBlurRadius(17)
        window.shadow.setXOffset(0)
        window.shadow.setYOffset(0)
        window.shadow.setColor(QColor(0, 0, 0, 150))
        window.ui.bgApp.setGraphicsEffect(window.shadow)

        window.sizegrip = QSizeGrip(window.ui.bottomBar.appSizeGrip)
        window.sizegrip.setStyleSheet(
            "width: 20px; height: 20px; margin 0px; padding: 0px;"
        )

        window.ui.headerContainer.minimizeAppBtn.clicked.connect(
            lambda: window.showMinimized()
        )
        window.ui.headerContainer.maximizeRestoreAppBtn.clicked.connect(
            lambda: WindowService.maximize_restore(window)
        )
        window.ui.headerContainer.closeAppBtn.clicked.connect(lambda: window.close())

    @staticmethod
    def resize_grips(window: Any) -> None:
        """Resize custom grips when the main window size changes."""
        if get_settings_service().app.ENABLE_CUSTOM_TITLE_BAR:
            window.left_grip.setGeometry(0, 10, 10, window.height())
            window.right_grip.setGeometry(window.width() - 10, 10, 10, window.height())
            window.top_grip.setGeometry(0, 0, window.width(), 10)
            window.bottom_grip.setGeometry(0, window.height() - 10, window.width(), 10)
