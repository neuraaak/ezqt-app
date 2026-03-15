# ///////////////////////////////////////////////////////////////
# WIDGETS.UI_MAIN - Main window user interface setup
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Ui_MainWindow — setupUi builder for the main application window."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtCore import QMetaObject, QSize
from PySide6.QtWidgets import QFrame, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

# Local imports
from ..services.settings import get_settings_service
from ..services.translation import get_translation_manager
from ..services.ui import Fonts
from ..widgets.core import BottomBar, Header, Menu, PageContainer, SettingsPanel


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class Ui_MainWindow:
    """
    Main application user interface.

    This class defines the structure of the main user interface
    with all its components (header, menu, content, etc.).
    """

    def __init__(self) -> None:
        """Initialize the main user interface."""

    def setupUi(self, MainWindow: QMainWindow) -> None:
        """
        Configure the main user interface.

        Parameters
        ----------
        MainWindow : QMainWindow
            The main window to configure.
        """
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QSize(940, 560))
        settings_service = get_settings_service()

        # ////// SETUP MAIN STYLESHEET WIDGET
        self.style_sheet = QWidget(MainWindow)
        self.style_sheet.setObjectName("style_sheet")
        if Fonts.SEGOE_UI_10_REG is not None:
            self.style_sheet.setFont(Fonts.SEGOE_UI_10_REG)

        # ////// SETUP MAIN MARGINS
        self.app_margins_layout = QVBoxLayout(self.style_sheet)
        self.app_margins_layout.setSpacing(0)
        self.app_margins_layout.setObjectName("app_margins_layout")
        self.app_margins_layout.setContentsMargins(10, 10, 10, 10)

        # ////// SETUP BACKGROUND APP
        self.bg_app_frame = QFrame(self.style_sheet)
        self.bg_app_frame.setObjectName("bg_app_frame")
        self.bg_app_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.bg_app_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.app_margins_layout.addWidget(self.bg_app_frame)

        # ////// SETUP APP LAYOUT
        self.app_layout = QVBoxLayout(self.bg_app_frame)
        self.app_layout.setSpacing(0)
        self.app_layout.setObjectName("app_layout")
        self.app_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP HEADER
        self.header_container = Header(parent=self.bg_app_frame)
        self.app_layout.addWidget(self.header_container)

        # ////// SETUP CONTENT BOTTOM (MIDDLE LAYER: MENU | CONTENT | SETTINGS)
        self.content_bottom_frame = QFrame(self.bg_app_frame)
        self.content_bottom_frame.setObjectName("content_bottom_frame")
        self.content_bottom_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.content_bottom_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.app_layout.addWidget(self.content_bottom_frame)

        # ////// SETUP CONTENT BOTTOM LAYOUT (HORIZONTAL)
        self.content_bottom_layout = QHBoxLayout(self.content_bottom_frame)
        self.content_bottom_layout.setSpacing(0)
        self.content_bottom_layout.setObjectName("content_bottom_layout")
        self.content_bottom_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP MENU
        self.menu_container = Menu(
            parent=self.content_bottom_frame,
            shrink_width=settings_service.gui.MENU_PANEL_SHRINKED_WIDTH,
            extended_width=settings_service.gui.MENU_PANEL_EXTENDED_WIDTH,
        )
        self.content_bottom_layout.addWidget(self.menu_container)

        # ////// SETUP CONTENT (CENTER)
        self.content_frame = QFrame(self.content_bottom_frame)
        self.content_frame.setObjectName("content_frame")
        self.content_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.content_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.content_bottom_layout.addWidget(self.content_frame, 1)

        # ////// SETUP CONTENT LAYOUT
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setSpacing(0)
        self.content_layout.setObjectName("content_layout")
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP PAGES CONTAINER
        self.pages_container = PageContainer(self.content_frame)
        self.content_layout.addWidget(self.pages_container)

        # ////// SETUP SETTINGS PANEL (RIGHT)
        self.settings_panel = SettingsPanel(
            parent=self.content_bottom_frame,
            width=settings_service.gui.SETTINGS_PANEL_WIDTH,
        )
        self.content_bottom_layout.addWidget(self.settings_panel)

        # ////// SETUP BOTTOM BAR (FULL WIDTH)
        self.bottom_bar = BottomBar(parent=self.bg_app_frame)
        self.app_layout.addWidget(self.bottom_bar)

        # ////// CONNECT TRANSLATION INDICATOR
        # Wire the TranslationManager signals to the BottomBar indicator so the
        # widget stays decoupled from the service (signal/slot, no direct reference).
        translation_manager = get_translation_manager()
        translation_manager.translation_started.connect(
            self.bottom_bar.show_translation_indicator
        )
        translation_manager.translation_finished.connect(
            self.bottom_bar.hide_translation_indicator
        )

        # ////// FINAL SETUP
        MainWindow.setCentralWidget(self.style_sheet)
        QMetaObject.connectSlotsByName(MainWindow)


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["Ui_MainWindow"]
