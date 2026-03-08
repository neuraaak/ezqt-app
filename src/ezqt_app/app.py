# ///////////////////////////////////////////////////////////////
# APP - Main application window
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""EzQt_App — Main QMainWindow subclass for EzQt applications."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import platform
import sys
from pathlib import Path
from typing import Any

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QPixmap, QResizeEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

# Local imports
from .services.application.app_service import AppService
from .services.config import get_config_service
from .services.settings import get_settings_service
from .services.translation import enable_auto_translation, get_translation_service
from .services.ui import (
    Fonts,
    MenuService,
    PanelService,
    SizePolicy,
    ThemeService,
    UiDefinitionsService,
)
from .shared.resources import Images
from .utils.diagnostics import warn_tech, warn_user
from .utils.printer import get_printer
from .widgets.core.ez_app import EzApplication
from .widgets.ui_main import Ui_MainWindow

# ///////////////////////////////////////////////////////////////
# GLOBALS
# ///////////////////////////////////////////////////////////////
os_name: str = platform.system()
widgets: Any | None = None

# ///////////////////////////////////////////////////////////////
# VARIABLES
# ///////////////////////////////////////////////////////////////
APP_PATH: Path = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))
_dev: bool = bool(not hasattr(sys, "frozen"))

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class EzQt_App(QMainWindow):
    """
    Main EzQt_App application.

    This class represents the main application window
    with all its components (menu, pages, settings, etc.).
    """

    def __init__(
        self,
        themeFileName: str | None = None,
    ) -> None:
        """
        Initialize the EzQt_App application.

        Parameters
        ----------
        themeFileName : str, optional
            Name of the theme file to use (default: None).
        """
        QMainWindow.__init__(self)

        # ////// APP SERVICE LOADER
        # ///////////////////////////////////////////////////////////////
        AppService.load_fonts_resources()
        AppService.load_app_settings()

        config_service = get_config_service()

        # ////// LOAD TRANSLATIONS
        # ///////////////////////////////////////////////////////////////
        # Load language from settings
        try:
            # Load default language from translation.config.yaml, then allow app override.
            default_language_code = "en"
            translation_config_data = config_service.load_config("translation")

            supported_languages = translation_config_data.get("supported_languages", [])
            supported_codes = {
                str(item.get("code", "")).lower()
                for item in supported_languages
                if isinstance(item, dict)
            }

            detection = translation_config_data.get("language_detection", {})
            if isinstance(detection, dict):
                default_language_code = str(
                    detection.get("default_source_language", "en")
                ).lower()

            if default_language_code not in supported_codes:
                warn_user(
                    code="app.language.invalid_default_source_language",
                    user_message=(
                        "Invalid default_source_language in translation config; "
                        "falling back to English"
                    ),
                    log_message=(
                        "default_source_language is not declared in supported_languages"
                    ),
                )
                default_language_code = "en"

            # Try to load settings_panel from app.config.yaml
            app_config = config_service.load_config("app")
            if "settings_panel" in app_config:
                settings_panel = app_config["settings_panel"]
                language_value = str(
                    settings_panel.get("language", {}).get(
                        "default", default_language_code
                    )
                )
            else:
                language_value = default_language_code

            translation_service = get_translation_service()
            # Accept both display names ("Français") and codes ("fr").
            if not translation_service.change_language(language_value):
                translation_service.change_language_by_code(language_value.lower())

            translation_config = translation_config_data.get("translation", {})
            auto_translation_flag = False
            if isinstance(translation_config, dict):
                raw_flag = translation_config.get("auto_translation_enabled", False)
                if isinstance(raw_flag, str):
                    auto_translation_flag = raw_flag.strip().lower() in {
                        "1",
                        "true",
                        "yes",
                        "on",
                    }
                else:
                    auto_translation_flag = bool(raw_flag)

            enable_auto_translation(auto_translation_flag)
        except Exception:
            translation_service = get_translation_service()
            translation_service.change_language("English")
            enable_auto_translation(False)

        # Keep registration/collection active for local TS workflow.
        # `auto_translation_enabled` only gates external API translation calls.

        # ////// INITIALIZE COMPONENTS
        # ///////////////////////////////////////////////////////////////
        Fonts.initFonts()
        SizePolicy.initSizePolicy()

        # ////// SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        settings_service = get_settings_service()

        # ////// USE CUSTOM TITLE BAR
        # ///////////////////////////////////////////////////////////////
        settings_service.set_custom_title_bar_enabled(os_name == "Windows")

        # ////// APP DATA
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(settings_service.app.NAME)
        (
            self.setAppIcon(Images.logo_placeholder, yShrink=0)
            if settings_service.gui.THEME == "dark"
            else self.setAppIcon(Images.logo_placeholder, yShrink=0)
        )

        # ==> TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.menuContainer.toggleButton.clicked.connect(
            lambda: PanelService.toggle_menu_panel(self, True)
        )

        # ==> TOGGLE SETTINGS
        # ///////////////////////////////////////////////////////////////
        widgets.headerContainer.settingsTopBtn.clicked.connect(
            lambda: PanelService.toggle_settings_panel(self, True)
        )

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UiDefinitionsService.apply_definitions(self)

        # SET THEME
        # ///////////////////////////////////////////////////////////////
        self._themeFileName = themeFileName
        ThemeService.apply_theme(self, self._themeFileName)
        # //////
        # Load theme from settings_panel if it exists, otherwise from app
        try:
            # Try to load settings_panel from app.config.yaml
            app_config = config_service.load_config("app")
            app_defaults = app_config.get("app", {})
            fallback_theme = str(app_defaults.get("theme", "dark"))
            if "settings_panel" in app_config:
                settings_panel = app_config["settings_panel"]
                _theme = settings_panel.get("theme", {}).get("default", fallback_theme)
            else:
                # Fallback to default value
                _theme = fallback_theme
            # Force conversion to lowercase
            _theme = _theme.lower()
        except Exception:
            # Fallback to default value
            _theme = "dark"

        # Update active theme with lowercase value
        settings_service.set_theme(_theme)

        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle and hasattr(theme_toggle, "initialize_selector"):
            try:
                # Convert theme value to ID
                theme_id = 0 if _theme == "light" else 1  # 0 = Light, 1 = Dark
                theme_toggle.initialize_selector(theme_id)
            except Exception as e:
                warn_tech(
                    code="app.theme.initialize_selector_failed",
                    message="Could not initialize theme selector",
                    error=e,
                )
        self.ui.headerContainer.update_all_theme_icons()
        self.ui.menuContainer.update_all_theme_icons()
        # //////
        if theme_toggle:
            # Connect valueChanged signal instead of clicked for new version
            if hasattr(theme_toggle, "valueChanged"):
                theme_toggle.valueChanged.connect(self.setAppTheme)
            elif hasattr(theme_toggle, "clicked"):
                theme_toggle.clicked.connect(self.setAppTheme)

        # ==> REGISTER ALL WIDGETS FOR TRANSLATION
        # ///////////////////////////////////////////////////////////////
        self._register_all_widgets_for_translation()

        # ==> COLLECT STRINGS FOR TRANSLATION
        # ///////////////////////////////////////////////////////////////
        self._collect_strings_for_translation()

    # SET APP THEME
    # ///////////////////////////////////////////////////////////////
    def setAppTheme(self) -> None:
        settings_service = get_settings_service()
        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle:
            # Handle both cases: valueChanged (string) and clicked (no parameter)
            if hasattr(theme_toggle, "value_id"):
                # Use value_id to get current ID
                theme_id = theme_toggle.value_id
                # Convert ID to theme value
                theme = "light" if theme_id == 0 else "dark"
            elif hasattr(theme_toggle, "value"):
                # Use value to get text value
                theme = theme_toggle.value.lower()
            else:
                # Fallback: use current settings service value
                theme = settings_service.gui.THEME

            # Update active theme
            settings_service.set_theme(theme)

            # Save directly to app.settings_panel.theme.default
            AppService.write_yaml_config(
                ["app", "settings_panel", "theme", "default"], theme
            )

            # Force immediate update
            self.updateUI()

    # UPDATE UI
    # ///////////////////////////////////////////////////////////////
    def updateUI(self) -> None:
        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle and hasattr(theme_toggle, "get_value_option"):
            # New OptionSelector version handles positioning automatically
            # No need for manual move_selector
            pass

        # //////
        ThemeService.apply_theme(self, self._themeFileName)
        # //////
        ez_app = EzApplication.instance()
        if isinstance(ez_app, EzApplication):
            ez_app.themeChanged.emit()
        self.ui.headerContainer.update_all_theme_icons()
        self.ui.menuContainer.update_all_theme_icons()
        self.ui.settingsPanel.update_all_theme_icons()

        # //////
        QApplication.processEvents()

        # Force refresh of all widgets
        app_instance = QApplication.instance()
        if isinstance(app_instance, QApplication):
            for widget in app_instance.allWidgets():
                widget.style().unpolish(widget)
                widget.style().polish(widget)

    # SET APP ICON
    # ///////////////////////////////////////////////////////////////
    def setAppIcon(
        self, icon: str | QPixmap, yShrink: int = 0, yOffset: int = 0
    ) -> None:
        return self.ui.headerContainer.set_app_logo(
            logo=icon, y_shrink=yShrink, y_offset=yOffset
        )

    # ADD MENU & PAGE
    # ///////////////////////////////////////////////////////////////
    def addMenu(self, name: str, icon: str) -> QWidget:
        page = self.ui.pagesContainer.add_page(name)
        # //////
        menu = self.ui.menuContainer.add_menu(name, icon)
        menu.setProperty("page", page)
        if len(self.ui.menuContainer.menus) == 1:
            menu.setProperty("class", "active")
        # //////
        menu.clicked.connect(
            lambda: self.ui.pagesContainer.stackedWidget.setCurrentWidget(page)
        )
        menu.clicked.connect(self.switchMenu)

        # //////
        return page

    # MENU SWITCH
    # ///////////////////////////////////////////////////////////////
    def switchMenu(self) -> None:
        # GET BUTTON CLICKED
        sender = self.sender()
        senderName = sender.objectName()

        # SHOW HOME PAGE
        for btnName, _ in self.ui.menuContainer.menus.items():
            if senderName == f"menu_{btnName}":
                MenuService.deselect_menu(self, senderName)
                MenuService.select_menu(self, senderName)

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: ARG002
        # Update Size Grips
        UiDefinitionsService.resize_grips(self)

    # REGISTER ALL WIDGETS FOR TRANSLATION
    # ///////////////////////////////////////////////////////////////
    def _register_all_widgets_for_translation(self) -> None:
        """Automatically register all widgets with text for translation."""
        try:
            # Safe import of translation functions
            try:
                from .services.translation import set_tr
                from .services.translation import tr as translate_text
            except ImportError as import_error:
                warn_tech(
                    code="app.translation.import_helpers_failed",
                    message="Could not import translation helpers",
                    error=import_error,
                )
                return

            registered_count = 0
            registered_widgets = set()  # To avoid duplicates

            def register_widget_recursive(widget):
                """Recursive function to register all widgets."""
                nonlocal registered_count

                try:
                    # Avoid already registered widgets
                    if widget in registered_widgets:
                        return

                    # Check if widget has text
                    if hasattr(widget, "text") and callable(
                        getattr(widget, "text", None)
                    ):
                        try:
                            text = widget.text().strip()
                            # Avoid widgets with technical text, numeric values, or too short
                            if (
                                text
                                and not text.isdigit()
                                and len(text) > 1
                                and not text.startswith("_")
                                and not text.startswith("menu_")
                                and not text.startswith("btn_")
                                and not text.startswith("setting")
                            ):
                                # Register widget for translation
                                set_tr(widget, text)
                                registered_widgets.add(widget)
                                registered_count += 1
                        except Exception as e:
                            warn_tech(
                                code="app.translation.read_widget_text_failed",
                                message=f"Could not read widget text for {type(widget)}",
                                error=e,
                            )

                    # Check tooltips
                    if hasattr(widget, "toolTip") and callable(
                        getattr(widget, "toolTip", None)
                    ):
                        try:
                            tooltip = widget.toolTip().strip()
                            if (
                                tooltip
                                and not tooltip.isdigit()
                                and len(tooltip) > 1
                                and not tooltip.startswith("_")
                            ):
                                # For tooltips, we can use setToolTip with tr()
                                widget.setToolTip(translate_text(tooltip))
                        except Exception as e:
                            warn_tech(
                                code="app.translation.read_widget_tooltip_failed",
                                message=f"Could not read widget tooltip for {type(widget)}",
                                error=e,
                            )

                    # Check placeholders
                    if hasattr(widget, "placeholderText") and callable(
                        getattr(widget, "placeholderText", None)
                    ):
                        try:
                            placeholder = widget.placeholderText().strip()
                            if (
                                placeholder
                                and not placeholder.isdigit()
                                and len(placeholder) > 1
                                and not placeholder.startswith("_")
                            ):
                                widget.setPlaceholderText(translate_text(placeholder))
                        except Exception as e:
                            warn_tech(
                                code="app.translation.read_widget_placeholder_failed",
                                message=(
                                    f"Could not read widget placeholder for {type(widget)}"
                                ),
                                error=e,
                            )

                    # Iterate through all children
                    try:
                        for child in widget.findChildren(QWidget):
                            register_widget_recursive(child)
                    except Exception as e:
                        warn_tech(
                            code="app.translation.iter_widget_children_failed",
                            message=(
                                f"Could not iterate children for widget {type(widget)}"
                            ),
                            error=e,
                        )
                except Exception as e:
                    warn_tech(
                        code="app.translation.scan_widget_failed",
                        message=f"Could not scan widget {type(widget)}",
                        error=e,
                    )

            # Start with main window
            register_widget_recursive(self)

            # Manually register specific widgets with fixed text
            self._register_specific_widgets_for_translation()
            get_printer().action(
                f"[EzQt_App] {registered_count} widgets registered for translation."
            )

        except Exception as e:
            warn_tech(
                code="app.translation.register_widgets_failed",
                message="Could not register widgets for translation",
                error=e,
            )

    def _register_specific_widgets_for_translation(self) -> None:
        """Manually register specific widgets with fixed text."""
        try:
            from .services.translation import set_tr

            # Widgets in ui_main.py with fixed text
            # Widgets in settings_panel with fixed text
            if hasattr(self.ui, "settingsPanel"):
                settings_panel = self.ui.settingsPanel

                # Register dynamically created settings widgets
                for widget in getattr(settings_panel, "_widgets", []):
                    if hasattr(widget, "label") and widget.label:
                        try:
                            text = widget.label.text()
                            if text and len(text) > 1:
                                set_tr(widget.label, text)
                        except Exception as e:
                            warn_tech(
                                code="app.translation.register_settings_widget_failed",
                                message="Could not register settings widget label",
                                error=e,
                            )

                # Register theme label
                if hasattr(settings_panel, "themeLabel"):
                    set_tr(settings_panel.themeLabel, "Theme")

                # Register theme selector options
                # OptionSelector version handles translations automatically

            # Widgets in menu with fixed text
            if hasattr(self.ui, "menuContainer"):
                menu_container = self.ui.menuContainer

                # Register dynamically created menu buttons
                for button in getattr(menu_container, "_buttons", []):
                    if hasattr(button, "text_label") and button.text_label:
                        try:
                            text = button.text_label.text()
                            if text and len(text) > 1:
                                set_tr(button.text_label, text)
                        except Exception as e:
                            warn_tech(
                                code="app.translation.register_menu_widget_failed",
                                message="Could not register menu widget label",
                                error=e,
                            )

            # Widgets in header with fixed text
            if hasattr(self.ui, "headerContainer"):
                header_container = self.ui.headerContainer

                # Register header labels
                if hasattr(header_container, "headerAppName"):
                    try:
                        text = header_container.headerAppName.text()
                        if text and len(text) > 1:
                            set_tr(header_container.headerAppName, text)
                    except Exception as e:
                        warn_tech(
                            code="app.translation.register_header_name_failed",
                            message="Could not register header app name",
                            error=e,
                        )

                if hasattr(header_container, "headerAppDescription"):
                    try:
                        text = header_container.headerAppDescription.text()
                        if text and len(text) > 1:
                            set_tr(header_container.headerAppDescription, text)
                    except Exception as e:
                        warn_tech(
                            code="app.translation.register_header_description_failed",
                            message="Could not register header app description",
                            error=e,
                        )

            # ezqt_widgets widgets with text
            # Note: These widgets generally handle their own translations
            # but we can register their text for automatic retranslation

            # ToggleSwitch widgets (in setting_widgets)
            # OptionSelector widgets (in settings_panel)
            # These widgets are already handled by automatic registration
        except Exception as e:
            warn_tech(
                code="app.translation.register_specific_widgets_failed",
                message="Could not register specific widgets for translation",
                error=e,
            )

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event: QMouseEvent) -> None:
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()

        # //////
        if _dev:
            # PRINT OBJECT NAME
            # //////
            child_widget = self.childAt(event.position().toPoint())
            if child_widget:
                child_name = child_widget.objectName()
                get_printer().verbose_msg(f"Mouse click on widget: {child_name}")

            # PRINT MOUSE EVENTS
            # //////
            elif event.buttons() == Qt.MouseButton.LeftButton:
                get_printer().verbose_msg("Mouse click: LEFT CLICK")
            elif event.buttons() == Qt.MouseButton.RightButton:
                get_printer().verbose_msg("Mouse click: RIGHT CLICK")

    def set_credits(self, credits):
        """
        Set the credits text in the bottom bar.
        Can be a simple string, a dict {"name": ..., "email": ...}, or a JSON string.
        """
        if hasattr(self.ui, "bottomBar") and self.ui.bottomBar:
            self.ui.bottomBar.set_credits(credits)

    def set_version(self, version):
        """
        Set the version text in the bottom bar.
        Can be a string ("1.0.0", "v1.0.0", etc).
        """
        if hasattr(self.ui, "bottomBar") and self.ui.bottomBar:
            self.ui.bottomBar.set_version(version)

    # TRANSLATION MANAGEMENT METHODS
    # ///////////////////////////////////////////////////////////////

    def scan_widgets_for_translation(self, widget=None, recursive=True):
        """
        Scan a widget to find translatable text.

        Parameters
        ----------
        widget : QWidget, optional
            Widget to scan (default: main window)
        recursive : bool
            If True, also scan child widgets

        Returns
        -------
        List[Tuple[QWidget, str]]
            List of tuples (widget, text) found
        """
        from .services.translation import scan_widgets_for_translation

        if widget is None:
            widget = self

        return scan_widgets_for_translation(widget, recursive)

    def register_widgets_manually(self, widgets_list):
        """
        Manually register a list of widgets for translation.

        Parameters
        ----------
        widgets_list : List[Tuple[QWidget, str]]
            List of tuples (widget, text) to register

        Returns
        -------
        int
            Number of widgets registered
        """
        from .services.translation import register_widgets_manually

        return register_widgets_manually(widgets_list)

    def scan_and_register_widgets(self, widget=None, recursive=True):
        """
        Scan a widget and automatically register all found widgets.

        Parameters
        ----------
        widget : QWidget, optional
            Widget to scan (default: main window)
        recursive : bool
            If True, also scan child widgets

        Returns
        -------
        int
            Number of widgets registered
        """
        from .services.translation import scan_and_register_widgets

        if widget is None:
            widget = self

        return scan_and_register_widgets(widget, recursive)

    def get_translation_stats(self):
        """
        Return complete translation system statistics.

        Returns
        -------
        dict
            Detailed statistics
        """
        from .services.translation import get_translation_stats

        return get_translation_stats()

    def enable_auto_translation(self, enabled=True):
        """
        Enable or disable automatic translation.

        Parameters
        ----------
        enabled : bool
            True to enable, False to disable
        """
        from .services.translation import enable_auto_translation

        enable_auto_translation(enabled)

    def clear_translation_cache(self):
        """Clear the automatic translation cache."""
        from .services.translation import clear_auto_translation_cache

        clear_auto_translation_cache()

    def _collect_strings_for_translation(self):
        """Automatically collect strings for translation."""
        try:
            from .services.translation import collect_and_compare_strings

            # Collect strings from entire application
            stats = collect_and_compare_strings(self, recursive=True)

            get_printer().info(
                f"[EzQt_App] Automatic collection completed: {stats['new_strings']} new strings found"
            )

        except Exception as e:
            warn_tech(
                code="app.translation.collect_strings_failed",
                message="Error during automatic string collection",
                error=e,
            )

    def collect_strings_for_translation(self, widget=None, recursive=True):
        """
        Collect character strings for translation.

        Parameters
        ----------
        widget : QWidget, optional
            Widget to scan (default: main window)
        recursive : bool
            If True, also scan child widgets

        Returns
        -------
        dict
            Collection statistics
        """
        from .services.translation import collect_and_compare_strings

        if widget is None:
            widget = self

        return collect_and_compare_strings(widget, recursive)

    def get_new_strings(self):
        """
        Return newly found strings.

        Returns
        -------
        set
            Set of new strings
        """
        from .services.translation import get_new_strings

        return get_new_strings()

    def mark_strings_as_registered(self, strings=None):
        """
        Mark strings as registered.

        Parameters
        ----------
        strings : set, optional
            Strings to mark (default: all new strings)
        """
        from .services.translation import mark_strings_as_registered

        mark_strings_as_registered(strings)

    def get_string_collector_stats(self):
        """
        Return string collector statistics.

        Returns
        -------
        dict
            Detailed statistics
        """
        from .services.translation import get_string_collector_stats

        return get_string_collector_stats()
