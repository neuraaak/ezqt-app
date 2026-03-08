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

        # ////// SETUP CONTENT BOX
        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName("contentBox")
        self.contentBox.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Shadow.Raised)
        self.appLayout.addWidget(self.contentBox)

        # ////// SETUP CONTENT BOX LAYOUT
        self.HL_contentBox = QHBoxLayout(self.contentBox)
        self.HL_contentBox.setSpacing(0)
        self.HL_contentBox.setObjectName("HL_contentBox")
        self.HL_contentBox.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP MENU
        self.menuContainer = Menu(
            parent=self.contentBox,
            shrink_width=settings_service.gui.MENU_PANEL_SHRINKED_WIDTH,
            extended_width=settings_service.gui.MENU_PANEL_EXTENDED_WIDTH,
        )
        self.HL_contentBox.addWidget(self.menuContainer)

        # ////// SETUP CONTENT BOTTOM
        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName("contentBottom")
        self.contentBottom.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Shadow.Raised)
        self.HL_contentBox.addWidget(self.contentBottom)

        # ////// SETUP CONTENT BOTTOM LAYOUT
        self.VL_contentBottom = QVBoxLayout(self.contentBottom)
        self.VL_contentBottom.setSpacing(0)
        self.VL_contentBottom.setObjectName("VL_contentBottom")
        self.VL_contentBottom.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP CONTENT
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName("content")
        self.content.setFrameShape(QFrame.Shape.NoFrame)
        self.content.setFrameShadow(QFrame.Shadow.Raised)
        self.VL_contentBottom.addWidget(self.content)

        # ////// SETUP CONTENT LAYOUT
        self.HL_content = QHBoxLayout(self.content)
        self.HL_content.setSpacing(0)
        self.HL_content.setObjectName("HL_content")
        self.HL_content.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP PAGE CONTAINER
        self.pagesContainer = PageContainer(self.contentBottom)
        self.HL_content.addWidget(self.pagesContainer)

        # ////// SETUP SETTINGS PANEL
        self.settingsPanel = SettingsPanel(
            parent=self.content,
            width=settings_service.gui.SETTINGS_PANEL_WIDTH,
        )
        self.HL_content.addWidget(self.settingsPanel)

        # ////// SETUP BOTTOM BAR
        self.bottomBar = BottomBar(parent=self.contentBottom)
        self.VL_contentBottom.addWidget(self.bottomBar)

        # ////// FINAL SETUP
        MainWindow.setCentralWidget(self.styleSheet)
        QMetaObject.connectSlotsByName(MainWindow)
