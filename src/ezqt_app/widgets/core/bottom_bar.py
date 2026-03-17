# ///////////////////////////////////////////////////////////////
# WIDGETS.CORE.BOTTOM_BAR - Application bottom bar widget
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""BottomBar widget with credits, version, and resize area."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import importlib.util
import re
import sys
from pathlib import Path

# Third-party imports
from PySide6.QtCore import QCoreApplication, QEvent, QSize, Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

# Local imports
from ...services.ui import Fonts
from ...utils.diagnostics import warn_tech


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class BottomBar(QFrame):
    """
    Bottom bar for the main window.

    This class provides a bottom bar with credits,
    version and resize area. Credits can be clickable
    and open an email client.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Initialize the bottom bar.

        Parameters
        ----------
        parent : Any, optional
            The parent widget (default: None).
        """
        super().__init__(parent)

        # ////// INITIALIZE TRANSLATION STORAGE
        # These are set by set_credits() and set_version() — initialised here
        # so retranslate_ui() can safely reference them before the setters run.
        self._default_credits: str = "Made with ❤️ by EzQt_App"
        self._credits_data: str | dict[str, str] = self._default_credits
        self._version_text: str = ""

        # ////// SETUP WIDGET PROPERTIES
        self.setObjectName("bottom_bar")
        self.setMinimumSize(QSize(0, 22))
        self.setMaximumSize(QSize(16777215, 22))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)

        # ////// SETUP MAIN LAYOUT
        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setObjectName("bottom_bar_layout")
        self._layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP CREDITS LABEL
        self._credits_label = QLabel(self)
        self._credits_label.setObjectName("credits_label")
        self._credits_label.setMaximumSize(QSize(16777215, 16))
        if Fonts.SEGOE_UI_10_REG is not None:
            self._credits_label.setFont(Fonts.SEGOE_UI_10_REG)
        self._credits_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self._layout.addWidget(self._credits_label)

        # ////// SETUP TRANSLATION SEPARATOR
        # Displayed only while the translation indicator is visible.
        self._trans_sep_label = QLabel(self)
        self._trans_sep_label.setObjectName("trans_sep_label")
        self._trans_sep_label.setMaximumSize(QSize(16777215, 16))
        if Fonts.SEGOE_UI_10_REG is not None:
            self._trans_sep_label.setFont(Fonts.SEGOE_UI_10_REG)
        self._trans_sep_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self._trans_sep_label.setText("•")
        self._trans_sep_label.setVisible(False)
        self._layout.addWidget(self._trans_sep_label)

        # ////// SETUP TRANSLATION INDICATOR LABEL
        # Shown only while async auto-translations are in flight.
        self._trans_ind_label = QLabel(self)
        self._trans_ind_label.setObjectName("trans_ind_label")
        self._trans_ind_label.setMaximumSize(QSize(16777215, 16))
        if Fonts.SEGOE_UI_10_REG is not None:
            self._trans_ind_label.setFont(Fonts.SEGOE_UI_10_REG)
        self._trans_ind_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        # Hidden by default — only visible while translations are pending.
        self._trans_ind_label.setVisible(False)
        self._layout.addWidget(self._trans_ind_label)

        # Push the version block to the right, keeping credits + indicator grouped left.
        self._layout.addStretch(1)

        # ////// SETUP VERSION LABEL
        self._version_label = QLabel(self)
        self._version_label.setObjectName("version_label")
        self._version_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignTrailing
            | Qt.AlignmentFlag.AlignVCenter
        )
        self._layout.addWidget(self._version_label)

        # ////// SETUP SIZE GRIP
        # Keeping variable name 'size_grip_spacer' for MainWindowProtocol compatibility.
        self.size_grip_spacer = QFrame(self)
        self.size_grip_spacer.setObjectName("size_grip_spacer")
        self.size_grip_spacer.setMinimumSize(QSize(20, 0))
        self.size_grip_spacer.setMaximumSize(QSize(20, 16777215))
        self.size_grip_spacer.setFrameShape(QFrame.Shape.NoFrame)
        self.size_grip_spacer.setFrameShadow(QFrame.Shadow.Raised)
        self._layout.addWidget(self.size_grip_spacer)

        # ////// INITIALIZE DEFAULT VALUES
        self.retranslate_ui()
        self.set_version_auto()

    # ///////////////////////////////////////////////////////////////
    # UTILITY FUNCTIONS

    def _tr(self, text: str) -> str:
        """Shortcut for translation with global context."""
        return QCoreApplication.translate("EzQt_App", text)

    def show_translation_indicator(self) -> None:
        """Show the translation-in-progress indicator in the bottom bar.

        Called via signal/slot when the first async auto-translation is enqueued.
        Safe to call from any thread that posts to the Qt event loop.
        """
        self._trans_sep_label.setVisible(True)
        self._trans_ind_label.setVisible(True)

    def hide_translation_indicator(self) -> None:
        """Hide the translation indicator once all pending translations are done.

        Called via signal/slot when the pending auto-translation count reaches zero.
        Safe to call from any thread that posts to the Qt event loop.
        """
        self._trans_sep_label.setVisible(False)
        self._trans_ind_label.setVisible(False)

    def set_credits(self, credits: str | dict[str, str]) -> None:
        """
        Set credits with support for simple text or dictionary.

        Parameters
        ----------
        credits : str or Dict[str, str]
            Credits as simple text or dictionary with 'name' and 'email'.
        """
        try:
            # Store original data so retranslate_ui() can re-apply on language change.
            self._credits_data = credits

            if isinstance(credits, dict):
                # Credits with name and email
                self._create_clickable_credits(credits)
            else:
                self._credits_label.setText(self._tr(credits))

        except Exception as e:
            warn_tech(
                code="widgets.bottom_bar.set_credits_failed",
                message="Could not apply credits data",
                error=e,
            )
            self._credits_label.setText(self._default_credits)

    def _create_clickable_credits(self, credits_data: dict[str, str]) -> None:
        """
        Create a clickable link for credits with name and email.

        Parameters
        ----------
        credits_data : Dict[str, str]
            Dictionary with 'name' and 'email'.
        """
        try:
            name = credits_data.get("name", "Unknown")
            email = credits_data.get("email", "")

            # Build translatable base text then append the name (untranslated).
            base = self._tr("Made with ❤️ by")
            credits_text = f"{base} {name}"

            self._credits_label.setText(credits_text)

            # Make label clickable if email is provided
            if email:
                self._credits_label.setCursor(Qt.CursorShape.PointingHandCursor)
                self._credits_label.mousePressEvent = lambda _event: self._open_email(  # type: ignore[method-assign]
                    email
                )
                self._credits_label.setStyleSheet(
                    "color: #0078d4; text-decoration: underline;"
                )
            else:
                self._credits_label.setCursor(Qt.CursorShape.ArrowCursor)
                self._credits_label.setStyleSheet("")

        except Exception as e:
            warn_tech(
                code="widgets.bottom_bar.create_clickable_credits_failed",
                message="Could not create clickable credits",
                error=e,
            )
            self._credits_label.setText(self._default_credits)

    def _open_email(self, email: str) -> None:
        """
        Open default email client with specified address.

        Parameters
        ----------
        email : str
            Email address to open.
        """
        try:
            QDesktopServices.openUrl(QUrl(f"mailto:{email}"))
        except Exception as e:
            warn_tech(
                code="widgets.bottom_bar.open_email_failed",
                message=f"Could not open mailto link for {email}",
                error=e,
            )

    def set_version_auto(self) -> None:
        """
        Automatically detect user project version.

        First look for __version__ in main module,
        otherwise use default value.
        """
        detected_version = self._detect_project_version()
        if detected_version:
            self.set_version(detected_version)
        else:
            # Fallback to EzQt_App version if no version found
            try:
                from ...version import __version__

                self.set_version(f"v{__version__}")
            except ImportError:
                self.set_version("")  # Default version

    def set_version_forced(self, version: str) -> None:
        """
        Force displayed version (ignore automatic detection).

        Parameters
        ----------
        version : str
            Version to display (ex: "v1.0.0" or "1.0.0").
        """
        self.set_version(version)

    def _detect_project_version(self) -> str | None:
        """
        Detect user project version by looking for __version__ in main.py.

        Returns
        -------
        str or None
            Detected version or None if not found.
        """
        try:
            # Method 1: Look in current directory
            main_py_path = Path.cwd() / "main.py"
            if main_py_path.exists():
                version = self._extract_version_from_file(main_py_path)
                if version:
                    return version

            # Method 2: Look in main script directory
            script_dir = Path(sys.argv[0]).parent if sys.argv else Path.cwd()
            main_py_path = script_dir / "main.py"
            if main_py_path.exists():
                version = self._extract_version_from_file(main_py_path)
                if version:
                    return version

            # Method 3: Look in parent directory (case where exe is in subfolder)
            parent_dir = Path.cwd().parent
            main_py_path = parent_dir / "main.py"
            if main_py_path.exists():
                version = self._extract_version_from_file(main_py_path)
                if version:
                    return version

            # Method 4: Try to import main module
            try:
                import importlib

                main_mod = importlib.import_module("main")
                if hasattr(main_mod, "__version__"):
                    return f"v{main_mod.__version__}"
            except ImportError:
                pass

            # Method 5: Fallback to EzQt_App version
            try:
                from ...version import __version__

                return f"v{__version__}"
            except ImportError:
                pass

            return None

        except Exception as e:
            warn_tech(
                code="widgets.bottom_bar.detect_project_version_failed",
                message="Could not detect project version",
                error=e,
            )
            # In case of error, return None
            return None

    def _extract_version_from_file(self, file_path: Path) -> str | None:
        """
        Extract version from a Python file.

        Parameters
        ----------
        file_path : Path
            Path to Python file.

        Returns
        -------
        str or None
            Extracted version or None if not found.
        """
        try:
            # Read file content
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Look for __version__ = "..." in content
            version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                return f"v{version_match.group(1)}"

            # If not found with regex, try to import module
            try:
                spec = importlib.util.spec_from_file_location("main", file_path)
                if spec and spec.loader:
                    main_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(main_module)

                    if hasattr(main_module, "__version__"):
                        return f"v{main_module.__version__}"
            except Exception as e:
                warn_tech(
                    code="widgets.bottom_bar.import_main_for_version_failed",
                    message=f"Could not import {file_path} to extract __version__",
                    error=e,
                )

            return None

        except Exception as e:
            warn_tech(
                code="widgets.bottom_bar.extract_version_failed",
                message=f"Could not extract version from {file_path}",
                error=e,
            )
            return None

    def set_version(self, text: str) -> None:
        """
        Set version text with translation system support.

        Parameters
        ----------
        text : str
            Version text (can be "v1.0.0" or just "1.0.0").
        """
        # Ensure version starts with "v"
        if not text.startswith("v"):
            text = f"v{text}"

        # Store so retranslate_ui() can re-apply the version string after a language
        # change (version strings are not translated, but the label must be refreshed).
        self._version_text = text
        self._version_label.setText(text)

    def retranslate_ui(self) -> None:
        """Apply current translations to all owned text labels."""
        # Re-apply credits through the standard setter so display logic is consistent.
        self.set_credits(self._credits_data)
        # Version strings are not translatable but must be refreshed on language change.
        if self._version_text:
            self._version_label.setText(self._version_text)
        # Refresh the indicator label text (visibility is unchanged here).
        self._trans_ind_label.setText(self._tr("Translating..."))

    def changeEvent(self, event: QEvent) -> None:
        """Handle Qt change events, triggering UI retranslation on language change.

        Parameters
        ----------
        event : QEvent
            The Qt change event.
        """
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["BottomBar"]
