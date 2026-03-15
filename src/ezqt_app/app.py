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
from typing import Any, cast

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QPixmap, QResizeEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

# Local imports
from .domain.ports.main_window import MainWindowProtocol
from .services.application.app_service import AppService
from .services.config import get_config_service
from .services.settings import get_settings_service
from .services.translation import get_translation_service
from .services.ui import (
    Fonts,
    MenuService,
    PanelService,
    SizePolicy,
    ThemeService,
    UiDefinitionsService,
)
from .shared.resources import Images
from .utils.diagnostics import warn_tech
from .utils.printer import get_printer
from .widgets.core.ez_app import EzApplication
from .widgets.ui_main import Ui_MainWindow

# ///////////////////////////////////////////////////////////////
# GLOBALS
# ///////////////////////////////////////////////////////////////
os_name: str = platform.system()

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

    def _as_window(self) -> MainWindowProtocol:
        """Cast self to MainWindowProtocol (EzQt_App is a QMainWindow satisfying the protocol)."""
        return cast(MainWindowProtocol, self)

    def __init__(
        self,
        theme_file_name: str | None = None,
        logs_dir: str | Path | None = None,
        log_file_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the EzQt_App application.

        Parameters
        ----------
        theme_file_name : str, optional
            Name of the theme file to use (default: None).
        logs_dir : str | Path, optional
            Custom logs directory overriding config/default path.
        log_file_name : str, optional
            Custom log file name overriding config/default naming.
        **kwargs : dict
            Backward compatibility for legacy arguments (e.g., themeFileName).
        """
        QMainWindow.__init__(self)

        # Handle backward compatibility
        if "themeFileName" in kwargs:
            warn_tech(
                code="app.legacy_arg",
                message="Argument 'themeFileName' is deprecated. Use 'theme_file_name' instead.",
            )
            theme_file_name = kwargs.pop("themeFileName")

        # ////// APP SERVICE LOADER
        # ///////////////////////////////////////////////////////////////
        AppService.load_fonts_resources()
        AppService.load_app_settings(
            logs_dir_override=logs_dir,
            log_file_name_override=log_file_name,
        )

        config_service = get_config_service()

        def _get_setting_default(
            config_data: dict[str, Any], key: str, fallback: str
        ) -> str:
            """Resolve a settings default from configured root with legacy fallback."""
            root = "settings_panel"
            app_section_raw = config_data.get("app")
            if isinstance(app_section_raw, dict):
                configured_root = app_section_raw.get("settings_storage_root")
                if isinstance(configured_root, str) and configured_root.strip():
                    root = configured_root.strip()

            def _read_nested(path_parts: list[str]) -> object | None:
                current: object = config_data
                for part in path_parts:
                    if not isinstance(current, dict) or part not in current:
                        return None
                    current = current[part]
                return current

            # 1) Configured storage root
            configured_parts = [part for part in root.split(".") if part]
            if configured_parts:
                configured_value = _read_nested([*configured_parts, key, "default"])
                if isinstance(configured_value, str) and configured_value.strip():
                    return configured_value.strip()

            # 2) Legacy root used by existing shipped config
            legacy_value = _read_nested(["settings_panel", key, "default"])
            if isinstance(legacy_value, str) and legacy_value.strip():
                return legacy_value.strip()

            # 3) New root used in some generated configs
            app_value = _read_nested(["app", "settings_panel", key, "default"])
            if isinstance(app_value, str) and app_value.strip():
                return app_value.strip()

            return fallback

        # ////// LOAD TRANSLATIONS
        # ///////////////////////////////////////////////////////////////
        # Language is read from settings_panel.language.default in app.config.yaml
        # (display name, e.g. "English"). "en" is the hardcoded ultimate fallback.
        try:
            app_config = config_service.load_config("app")
            language_value = _get_setting_default(app_config, "language", "en")

            translation_service = get_translation_service()
            # Accept both display names ("Français") and codes ("fr").
            if not translation_service.change_language(language_value):
                translation_service.change_language_by_code(language_value.lower())
        except Exception as e:
            warn_tech(
                code="app.language.load_failed",
                message="Failed to load language configuration; falling back to English",
                error=e,
            )
            get_translation_service().change_language("English")

        # ////// INITIALIZE COMPONENTS
        # ///////////////////////////////////////////////////////////////
        Fonts.initFonts()
        SizePolicy.initSizePolicy()

        # ////// SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        settings_service = get_settings_service()

        # ////// USE CUSTOM TITLE BAR
        # ///////////////////////////////////////////////////////////////
        settings_service.set_custom_title_bar_enabled(os_name == "Windows")

        # ////// APP DATA
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(settings_service.app.NAME)
        self.set_app_icon(Images.logo_placeholder, y_shrink=0)

        # ==> TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        self.ui.menu_container.toggle_button.clicked.connect(
            lambda: PanelService.toggle_menu_panel(self._as_window(), True)
        )

        # ==> TOGGLE SETTINGS
        # ///////////////////////////////////////////////////////////////
        self.ui.header_container.settings_btn.clicked.connect(
            lambda: PanelService.toggle_settings_panel(self._as_window(), True)
        )

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UiDefinitionsService.apply_definitions(self)

        # SET THEME
        # ///////////////////////////////////////////////////////////////
        self._theme_file_name = theme_file_name

        # Load theme from settings_panel if it exists, otherwise from app
        try:
            app_config = config_service.load_config("app")
            app_defaults = app_config.get("app", {})
            fallback_theme = str(app_defaults.get("theme", "dark"))
            _theme = _get_setting_default(app_config, "theme", fallback_theme)
            # Force conversion to lowercase
            _theme = _theme.lower()
        except Exception as e:
            warn_tech(
                code="app.theme.load_failed",
                message="Failed to load theme configuration; falling back to dark",
                error=e,
            )
            _theme = "dark"

        # Update active theme with lowercase value
        settings_service.set_theme(_theme)

        # Apply stylesheet after active theme has been resolved.
        ThemeService.apply_theme(self._as_window(), self._theme_file_name)

        theme_toggle = self.ui.settings_panel.get_theme_selector()
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
        self.ui.header_container.update_all_theme_icons()
        self.ui.menu_container.update_all_theme_icons()
        # //////
        if theme_toggle:
            # Connect valueChanged signal instead of clicked for new version
            if hasattr(theme_toggle, "valueChanged"):
                theme_toggle.valueChanged.connect(self.set_app_theme)
            elif hasattr(theme_toggle, "clicked"):
                theme_toggle.clicked.connect(self.set_app_theme)

        # ==> COLLECT STRINGS FOR TRANSLATION (opt-in)
        # ///////////////////////////////////////////////////////////////
        # Only run if explicitly enabled via translation.collect_strings = true
        # in translation.config.yaml. Disabled by default to avoid unwanted filesystem
        # writes (pending_strings.txt, language_detected.txt, translation_tasks.json)
        # on every application startup.
        try:
            _translation_cfg = config_service.load_config("translation")
            _translation_section = _translation_cfg.get("translation", {})
            _collect_enabled = bool(
                _translation_section.get("collect_strings", False)
                if isinstance(_translation_section, dict)
                else False
            )
        except Exception:
            _collect_enabled = False

        if _collect_enabled:
            self._collect_strings_for_translation()

    # ///////////////////////////////////////////////////////////////
    # BACKWARD COMPATIBILITY ALIASES (DEPRECATED)
    # ///////////////////////////////////////////////////////////////

    def setAppTheme(self) -> None:
        """Deprecated alias for set_app_theme."""
        warn_tech(
            code="app.legacy_method",
            message="Method 'setAppTheme' is deprecated. Use 'set_app_theme' instead.",
        )
        self.set_app_theme()

    def updateUI(self) -> None:
        """Deprecated alias for update_ui."""
        warn_tech(
            code="app.legacy_method",
            message="Method 'updateUI' is deprecated. Use 'update_ui' instead.",
        )
        self.update_ui()

    def setAppIcon(
        self, logo: str | QPixmap, y_shrink: int = 0, y_offset: int = 0
    ) -> None:
        """Deprecated alias for set_app_icon."""
        warn_tech(
            code="app.legacy_method",
            message="Method 'setAppIcon' is deprecated. Use 'set_app_icon' instead.",
        )
        self.set_app_icon(logo, y_shrink, y_offset)

    def addMenu(self, name: str, icon: str) -> QWidget:
        """Deprecated alias for add_menu."""
        warn_tech(
            code="app.legacy_method",
            message="Method 'addMenu' is deprecated. Use 'add_menu' instead.",
        )
        return self.add_menu(name, icon)

    def switchMenu(self) -> None:
        """Deprecated alias for switch_menu."""
        warn_tech(
            code="app.legacy_method",
            message="Method 'switchMenu' is deprecated. Use 'switch_menu' instead.",
        )
        self.switch_menu()

    # ///////////////////////////////////////////////////////////////
    # NEW SNAKE_CASE METHODS
    # ///////////////////////////////////////////////////////////////

    def set_app_theme(self) -> None:
        settings_service = get_settings_service()
        theme_toggle = self.ui.settings_panel.get_theme_selector()
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

            # Stage theme change; flushed to disk on application quit.
            AppService.stage_config_value(
                ["app", "settings_panel", "theme", "default"], theme
            )

            # Force immediate update
            self.update_ui()

    # UPDATE UI
    # ///////////////////////////////////////////////////////////////
    def update_ui(self) -> None:
        theme_toggle = self.ui.settings_panel.get_theme_selector()
        if theme_toggle and hasattr(theme_toggle, "get_value_option"):
            # New OptionSelector version handles positioning automatically
            # No need for manual move_selector
            pass

        # //////
        ThemeService.apply_theme(self._as_window(), self._theme_file_name)
        # //////
        ez_app = EzApplication.instance()
        if isinstance(ez_app, EzApplication):
            ez_app.themeChanged.emit()
        self.ui.header_container.update_all_theme_icons()
        self.ui.menu_container.update_all_theme_icons()
        self.ui.settings_panel.update_all_theme_icons()

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
    def set_app_icon(
        self, icon: str | QPixmap, y_shrink: int = 0, y_offset: int = 0
    ) -> None:
        return self.ui.header_container.set_app_logo(
            logo=icon, y_shrink=y_shrink, y_offset=y_offset
        )

    # ADD MENU & PAGE
    # ///////////////////////////////////////////////////////////////
    def add_menu(self, name: str, icon: str) -> QWidget:
        page = self.ui.pages_container.add_page(name)
        # //////
        menu = self.ui.menu_container.add_menu(name, icon)
        menu.setProperty("page", page)
        if len(self.ui.menu_container.menus) == 1:
            menu.setProperty("class", "active")
        # //////
        menu.clicked.connect(lambda: self.ui.pages_container.set_current_widget(page))
        menu.clicked.connect(self.switch_menu)

        # //////
        return page

    # MENU SWITCH
    # ///////////////////////////////////////////////////////////////
    def switch_menu(self) -> None:
        # GET BUTTON CLICKED
        sender = self.sender()
        senderName = sender.objectName()

        # SHOW HOME PAGE
        for btnName, _ in self.ui.menu_container.menus.items():
            if senderName == f"menu_{btnName}":
                MenuService.deselect_menu(self._as_window(), senderName)
                MenuService.select_menu(self._as_window(), senderName)

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: ARG002
        # Update Size Grips
        UiDefinitionsService.resize_grips(self._as_window())

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
        if hasattr(self.ui, "bottom_bar") and self.ui.bottom_bar:
            self.ui.bottom_bar.set_credits(credits)

    def set_version(self, version):
        """
        Set the version text in the bottom bar.
        Can be a string ("1.0.0", "v1.0.0", etc).
        """
        if hasattr(self.ui, "bottom_bar") and self.ui.bottom_bar:
            self.ui.bottom_bar.set_version(version)

    # TRANSLATION MANAGEMENT METHODS
    # ///////////////////////////////////////////////////////////////

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

            get_printer().debug_msg(
                "[TranslationService] Automatic collection completed: "
                f"{stats['new_strings']} new strings found"
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
