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
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName("styleSheet")
        if Fonts.SEGOE_UI_10_REG is not None:
            self.styleSheet.setFont(Fonts.SEGOE_UI_10_REG)

        # ////// SETUP MAIN MARGINS
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName("appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)

        # ////// SETUP BACKGROUND APP
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName("bgApp")
        self.bgApp.setStyleSheet("")
        self.bgApp.setFrameShape(QFrame.Shape.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Shadow.Raised)
        self.appMargins.addWidget(self.bgApp)

        # ////// SETUP APP LAYOUT
        self.appLayout = QVBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName("appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP HEADER
        self.headerContainer = Header(parent=self.bgApp)
        self.appLayout.addWidget(self.headerContainer)

        # ////// SETUP CONTENT BOTTOM (MIDDLE LAYER: MENU | CONTENT | SETTINGS)
        self.contentBottom = QFrame(self.bgApp)
        self.contentBottom.setObjectName("contentBottom")
        self.contentBottom.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Shadow.Raised)
        self.appLayout.addWidget(self.contentBottom)

        # Backward-compatibility aliases kept for existing consumers/custom code.
        self.contentBox = self.contentBottom

        # ////// SETUP CONTENT BOTTOM LAYOUT (HORIZONTAL)
        self.HL_contentBottom = QHBoxLayout(self.contentBottom)
        self.HL_contentBottom.setSpacing(0)
        self.HL_contentBottom.setObjectName("HL_contentBottom")
        self.HL_contentBottom.setContentsMargins(0, 0, 0, 0)

        # Backward-compatibility alias kept for existing consumers/custom code.
        self.HL_contentBox = self.HL_contentBottom

        # ////// SETUP MENU
        self.menuContainer = Menu(
            parent=self.contentBottom,
            shrink_width=settings_service.gui.MENU_PANEL_SHRINKED_WIDTH,
            extended_width=settings_service.gui.MENU_PANEL_EXTENDED_WIDTH,
        )
        self.HL_contentBottom.addWidget(self.menuContainer)

        # ////// SETUP CONTENT (CENTER)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName("content")
        self.content.setFrameShape(QFrame.Shape.NoFrame)
        self.content.setFrameShadow(QFrame.Shadow.Raised)
        self.HL_contentBottom.addWidget(self.content, 1)

        # ////// SETUP CONTENT LAYOUT
        self.HL_content = QHBoxLayout(self.content)
        self.HL_content.setSpacing(0)
        self.HL_content.setObjectName("HL_content")
        self.HL_content.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP PAGE CONTAINER
        self.pagesContainer = PageContainer(self.content)
        self.HL_content.addWidget(self.pagesContainer)

        # ////// SETUP SETTINGS PANEL (RIGHT)
        self.settingsPanel = SettingsPanel(
            parent=self.contentBottom,
            width=settings_service.gui.SETTINGS_PANEL_WIDTH,
        )
        self.HL_contentBottom.addWidget(self.settingsPanel)

        # ////// SETUP BOTTOM BAR (FULL WIDTH)
        self.bottomBar = BottomBar(parent=self.bgApp)
        self.appLayout.addWidget(self.bottomBar)

        # ////// CONNECT TRANSLATION INDICATOR
        # Wire the TranslationManager signals to the BottomBar indicator so the
        # widget stays decoupled from the service (signal/slot, no direct reference).
        translation_manager = get_translation_manager()
        translation_manager.translation_started.connect(
            self.bottomBar.show_translation_indicator
        )
        translation_manager.translation_finished.connect(
            self.bottomBar.hide_translation_indicator
        )

        # ////// FINAL SETUP
        MainWindow.setCentralWidget(self.styleSheet)
        QMetaObject.connectSlotsByName(MainWindow)
