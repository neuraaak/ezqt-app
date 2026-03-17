# ///////////////////////////////////////////////////////////////
# WIDGETS.CORE.PAGE_CONTAINER - Page container widget
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""PageContainer widget with stacked widget page management."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtWidgets import QFrame, QStackedWidget, QVBoxLayout, QWidget


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class PageContainer(QFrame):
    """
    Page container with stacked widget management.

    This class provides a container to manage multiple pages
    within a central receptacle using a QStackedWidget.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Initialize the page container.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget (default: None).
        """
        super().__init__(parent)
        self.pages: dict[str, QWidget] = {}

        # ////// SETUP WIDGET PROPERTIES
        self.setObjectName("pages_container")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)

        # ////// SETUP MAIN LAYOUT
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setObjectName("pages_container_layout")
        self._layout.setContentsMargins(10, 10, 10, 10)

        # ////// SETUP STACKED WIDGET
        self._stacked_widget = QStackedWidget(self)
        self._stacked_widget.setObjectName("pages_stacked_widget")
        self._layout.addWidget(self._stacked_widget)

    # ///////////////////////////////////////////////////////////////
    # PUBLIC API

    def add_page(self, name: str) -> QWidget:
        """
        Add a new page to the container.

        Parameters
        ----------
        name : str
            The name of the page to add.

        Returns
        -------
        QWidget
            The created page widget.
        """
        page = QWidget()
        page.setObjectName(f"page_{name}")

        self._stacked_widget.addWidget(page)
        self.pages[name] = page

        return page

    def set_current_widget(self, widget: QWidget) -> None:
        """
        Set the current visible page.

        Parameters
        ----------
        widget : QWidget
            The page widget to display.
        """
        self._stacked_widget.setCurrentWidget(widget)

    def get_stacked_widget(self) -> QStackedWidget:
        """
        Access the internal stacked widget.

        Note: Use set_current_widget for standard navigation.
        """
        return self._stacked_widget


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["PageContainer"]
