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
from PySide6.QtGui import QMouseEvent, QPixmap, QResizeEvent, QShowEvent
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
# CONSTANTS
# ///////////////////////////////////////////////////////////////

OS_NAME: str = platform.system()
APP_PATH: Path = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))
IS_DEV: bool = bool(not hasattr(sys, "frozen"))

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class EzQt_App(QMainWindow):
    """
    Main EzQt_App application.

    This class represents the main application window
    with all its components (menu, pages, settings, etc.).
    """

    # ///////////////////////////////////////////////////////////////
    # INIT
    # ///////////////////////////////////////////////////////////////

    def __init__(
        self,
        theme_file_name: str | None = None,
        logs_dir: str | Path | None = None,
        log_file_name: str | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the EzQt_App application.

        Args:
            theme_file_name: Name of the theme file to use (default: None).
            logs_dir: Custom logs directory overriding config/default path.
            log_file_name: Custom log file name overriding config/default naming.
            **kwargs: Backward compatibility for legacy arguments (e.g., themeFileName).
        """
        QMainWindow.__init__(self)
        self._has_menu: bool = True
        self._has_settings_panel: bool = True
        self._ui_initialized: bool = False
        self._theme_file_name: str | None = theme_file_name

        # Handle backward compatibility
        if "themeFileName" in kwargs:
            warn_tech(
                code="app.legacy_arg",
                message="Argument 'themeFileName' is deprecated. Use 'theme_file_name' instead.",
            )
            theme_file_name = kwargs.pop("themeFileName")
            self._theme_file_name = theme_file_name

        # Load resources and settings
        AppService.load_fonts_resources()
        AppService.load_app_settings(
            logs_dir_override=logs_dir,
            log_file_name_override=log_file_name,
        )

        self._config_service = get_config_service()

    # ///////////////////////////////////////////////////////////////
    # PUBLIC METHODS
    # ///////////////////////////////////////////////////////////////

    def no_menu(self) -> EzQt_App:
        """
        Disable the left menu for this application instance.

        Returns:
            EzQt_App: Self instance for chaining.
        """
        self._has_menu = False
        return self

    def no_settings_panel(self) -> EzQt_App:
        """
        Disable the settings slide-in panel for this application instance.

        Returns:
            EzQt_App: Self instance for chaining.
        """
        self._has_settings_panel = False
        return self

    def build(self) -> EzQt_App:
        """
        Explicitly build the UI layout.

        Automatically called on first show() if not called.

        Returns:
            EzQt_App: Self instance for chaining.
        """
        if not self._ui_initialized:
            self._build_ui()
        return self

    def showEvent(self, event: QShowEvent) -> None:
        """
        Ensure UI is built before showing the window.

        Args:
            event: The QShowEvent instance.
        """
        if not self._ui_initialized:
            self._build_ui()
        super().showEvent(event)

    def set_app_theme(self) -> None:
        """Update and apply the application theme based on current settings."""
        self.build()
        settings_service = get_settings_service()
        theme_toggle = self.ui.settings_panel.get_theme_selector()
        if theme_toggle:
            if hasattr(theme_toggle, "value_id"):
                theme_id = theme_toggle.value_id
                theme = "light" if theme_id == 0 else "dark"
            elif hasattr(theme_toggle, "value"):
                theme = theme_toggle.value.lower()
            else:
                theme = settings_service.gui.THEME

            settings_service.set_theme(theme)
            AppService.stage_config_value(
                ["app", "settings_panel", "theme", "default"], theme
            )
            self.update_ui()

    def update_ui(self) -> None:
        """Force a full UI refresh including themes, icons, and styles."""
        self.build()
        ThemeService.apply_theme(self._as_window(), self._theme_file_name)
        ez_app = EzApplication.instance()
        if isinstance(ez_app, EzApplication):
            ez_app.themeChanged.emit()
        self.ui.header_container.update_all_theme_icons()
        self.ui.menu_container.update_all_theme_icons()
        self.ui.settings_panel.update_all_theme_icons()

        QApplication.processEvents()
        app_instance = QApplication.instance()
        if isinstance(app_instance, QApplication):
            for widget in app_instance.allWidgets():
                widget.style().unpolish(widget)
                widget.style().polish(widget)

    def set_app_icon(
        self, icon: str | QPixmap, y_shrink: int = 0, y_offset: int = 0
    ) -> None:
        """
        Set the application logo in the header.

        Args:
            icon: Path to icon or QPixmap object.
            y_shrink: Vertical shrink factor.
            y_offset: Vertical offset adjustment.
        """
        self.build()
        return self.ui.header_container.set_app_logo(
            logo=icon, y_shrink=y_shrink, y_offset=y_offset
        )

    def add_menu(self, name: str, icon: str) -> QWidget:
        """
        Add a new menu item and corresponding page.

        Args:
            name: Label for the menu and page.
            icon: Icon name or path.

        Returns:
            QWidget: The created page widget.
        """
        self.build()
        page = self.ui.pages_container.add_page(name)
        menu = self.ui.menu_container.add_menu(name, icon)
        menu.setProperty("page", page)
        if len(self.ui.menu_container.menus) == 1:
            menu.setProperty("class", "active")
        menu.clicked.connect(lambda: self.ui.pages_container.set_current_widget(page))
        menu.clicked.connect(self.switch_menu)

        return page

    def switch_menu(self) -> None:
        """Update active state of menu buttons based on sender."""
        sender = self.sender()
        if not sender:
            return
        senderName = sender.objectName()

        for btnName, _ in self.ui.menu_container.menus.items():
            if senderName == f"menu_{btnName}":
                MenuService.deselect_menu(self._as_window(), senderName)
                MenuService.select_menu(self._as_window(), senderName)

    def resizeEvent(self, _event: QResizeEvent) -> None:
        """
        Handle window resize events to update UI components.

        Args:
            _event: The QResizeEvent instance (unused).
        """
        if self._ui_initialized:
            UiDefinitionsService.resize_grips(self._as_window())

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse press events for window dragging and diagnostics.

        Args:
            event: The QMouseEvent instance.
        """
        if not self._ui_initialized:
            return
        self.dragPos = event.globalPosition().toPoint()
        if IS_DEV:
            child_widget = self.childAt(event.position().toPoint())
            if child_widget:
                child_name = child_widget.objectName()
                get_printer().verbose_msg(f"Mouse click on widget: {child_name}")
            elif event.buttons() == Qt.MouseButton.LeftButton:
                get_printer().verbose_msg("Mouse click: LEFT CLICK")
            elif event.buttons() == Qt.MouseButton.RightButton:
                get_printer().verbose_msg("Mouse click: RIGHT CLICK")

    def set_credits(self, credits: Any) -> None:
        """
        Set credit text in the bottom bar.

        Args:
            credits: Text or object to display as credits.
        """
        if hasattr(self.ui, "bottom_bar") and self.ui.bottom_bar:
            self.ui.bottom_bar.set_credits(credits)

    def set_version(self, version: str) -> None:
        """
        Set version text in the bottom bar.

        Args:
            version: Version string to display.
        """
        if hasattr(self.ui, "bottom_bar") and self.ui.bottom_bar:
            self.ui.bottom_bar.set_version(version)

    def get_translation_stats(self) -> dict[str, Any]:
        """
        Retrieve current translation statistics.

        Returns:
            dict: Statistics about translated and missing strings.
        """
        from .services.translation import get_translation_stats

        return get_translation_stats()

    def enable_auto_translation(self, enabled: bool = True) -> None:
        """
        Enable or disable automatic translation collection.

        Args:
            enabled: Whether to enable auto-translation.
        """
        from .services.translation import enable_auto_translation

        enable_auto_translation(enabled)

    def clear_translation_cache(self) -> None:
        """Clear the automatic translation cache."""
        from .services.translation import clear_auto_translation_cache

        clear_auto_translation_cache()

    def collect_strings_for_translation(
        self, widget: QWidget | None = None, recursive: bool = True
    ) -> dict[str, Any]:
        """
        Scan widgets for translatable strings and add them to the collector.

        Args:
            widget: Root widget to start scanning from (default: self).
            recursive: Whether to scan child widgets recursively.

        Returns:
            dict: Summary of the collection process.
        """
        from .services.translation import collect_and_compare_strings

        if widget is None:
            widget = self
        return collect_and_compare_strings(widget, recursive)

    def get_new_strings(self) -> set[str]:
        """
        Get all newly discovered strings since last save.

        Returns:
            set[str]: Set of new translatable strings.
        """
        from .services.translation import get_new_strings

        return get_new_strings()

    def get_string_collector_stats(self) -> dict[str, Any]:
        """
        Get statistics from the string collector.

        Returns:
            dict: Collector statistics.
        """
        from .services.translation import get_string_collector_stats

        return get_string_collector_stats()

    # ///////////////////////////////////////////////////////////////
    # PRIVATE METHODS
    # ///////////////////////////////////////////////////////////////

    def _as_window(self) -> MainWindowProtocol:
        """
        Cast self to MainWindowProtocol.

        Returns:
            MainWindowProtocol: Typed reference to self.
        """
        return cast(MainWindowProtocol, self)

    def _get_setting_default(
        self, config_data: dict[str, Any], key: str, fallback: str
    ) -> str:
        """
        Resolve a settings default from configured root with legacy fallback.

        Args:
            config_data: Full configuration dictionary.
            key: Setting key to look for.
            fallback: Value to return if key is not found.

        Returns:
            str: The resolved setting value.
        """
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

    def _build_ui(self) -> None:
        """Internal UI construction and orchestration."""
        if getattr(self, "_is_building", False):
            return
        self._is_building = True

        try:
            # Load translations
            app_config = self._config_service.load_config("app")
            language_value = self._get_setting_default(app_config, "language", "en")

            translation_service = get_translation_service()
            if not translation_service.change_language(language_value):
                translation_service.change_language_by_code(language_value.lower())
        except Exception as e:
            warn_tech(
                code="app.language.load_failed",
                message="Failed to load language configuration; falling back to English",
                error=e,
            )
            get_translation_service().change_language("English")

        # Initialize base components
        Fonts.initFonts()
        SizePolicy.initSizePolicy()

        # Set as global widgets
        self.ui = Ui_MainWindow()
        self.ui.setupUi(
            self,
            has_menu=self._has_menu,
            has_settings_panel=self._has_settings_panel,
        )

        settings_service = get_settings_service()

        # Use custom title bar on Windows
        settings_service.set_custom_title_bar_enabled(OS_NAME == "Windows")

        # Set application basic info
        self.setWindowTitle(settings_service.app.NAME)
        self.set_app_icon(Images.logo_placeholder, y_shrink=0)

        # Toggle Menu connection
        if self._has_menu and self.ui.menu_container.toggle_button:
            self.ui.menu_container.toggle_button.clicked.connect(
                lambda: PanelService.toggle_menu_panel(self._as_window(), True)
            )

        # Toggle Settings connection
        if self._has_settings_panel:
            self.ui.header_container.settings_btn.clicked.connect(
                lambda: PanelService.toggle_settings_panel(self._as_window(), True)
            )
        else:
            self.ui.header_container.settings_btn.hide()

        # Apply UI definitions and themes
        UiDefinitionsService.apply_definitions(self)

        try:
            app_config = self._config_service.load_config("app")
            app_defaults = app_config.get("app", {})
            fallback_theme = str(app_defaults.get("theme", "dark"))
            _theme = self._get_setting_default(app_config, "theme", fallback_theme)
            _theme = _theme.lower()
        except Exception as e:
            warn_tech(
                code="app.theme.load_failed",
                message="Failed to load theme configuration; falling back to dark",
                error=e,
            )
            _theme = "dark"

        settings_service.set_theme(_theme)
        ThemeService.apply_theme(self._as_window(), self._theme_file_name)

        # Theme selector initialization
        theme_toggle = self.ui.settings_panel.get_theme_selector()
        if theme_toggle and hasattr(theme_toggle, "initialize_selector"):
            try:
                theme_id = 0 if _theme == "light" else 1
                theme_toggle.initialize_selector(theme_id)
            except Exception as e:
                warn_tech(
                    code="app.theme.initialize_selector_failed",
                    message="Could not initialize theme selector",
                    error=e,
                )
        self.ui.header_container.update_all_theme_icons()
        self.ui.menu_container.update_all_theme_icons()

        if theme_toggle:
            if hasattr(theme_toggle, "valueChanged"):
                theme_toggle.valueChanged.connect(self.set_app_theme)
            elif hasattr(theme_toggle, "clicked"):
                theme_toggle.clicked.connect(self.set_app_theme)

        # String collection for translation
        try:
            _translation_cfg = self._config_service.load_config("translation")
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

        self._ui_initialized = True

    def _collect_strings_for_translation(self) -> None:
        """Internal helper for automatic string collection."""
        try:
            from .services.translation import collect_and_compare_strings

            stats = collect_and_compare_strings(self, recursive=True)
            get_printer().debug_msg(
                f"[TranslationService] Automatic collection completed: {stats['new_strings']} new strings found"
            )
        except Exception as e:
            warn_tech(
                code="app.translation.collect_strings_failed",
                message="Error during automatic string collection",
                error=e,
            )

    # ///////////////////////////////////////////////////////////////
    # BACKWARD COMPATIBILITY ALIASES (DEPRECATED)
    # ///////////////////////////////////////////////////////////////

    def setAppTheme(self) -> None:
        """
        Deprecated alias for set_app_theme.
        .. deprecated:: 1.0.0
        """
        warn_tech(
            code="app.legacy_method",
            message="Method 'setAppTheme' is deprecated. Use 'set_app_theme' instead.",
        )
        self.set_app_theme()

    def updateUI(self) -> None:
        """
        Deprecated alias for update_ui.
        .. deprecated:: 1.0.0
        """
        warn_tech(
            code="app.legacy_method",
            message="Method 'updateUI' is deprecated. Use 'update_ui' instead.",
        )
        self.update_ui()

    def setAppIcon(
        self, logo: str | QPixmap, y_shrink: int = 0, y_offset: int = 0
    ) -> None:
        """
        Deprecated alias for set_app_icon.
        .. deprecated:: 1.0.0
        """
        warn_tech(
            code="app.legacy_method",
            message="Method 'setAppIcon' is deprecated. Use 'set_app_icon' instead.",
        )
        self.set_app_icon(logo, y_shrink, y_offset)

    def addMenu(self, name: str, icon: str) -> QWidget:
        """
        Deprecated alias for add_menu.
        .. deprecated:: 1.0.0
        """
        warn_tech(
            code="app.legacy_method",
            message="Method 'addMenu' is deprecated. Use 'add_menu' instead.",
        )
        return self.add_menu(name, icon)

    def switchMenu(self) -> None:
        """
        Deprecated alias for switch_menu.
        .. deprecated:: 1.0.0
        """
        warn_tech(
            code="app.legacy_method",
            message="Method 'switchMenu' is deprecated. Use 'switch_menu' instead.",
        )
        self.switch_menu()
