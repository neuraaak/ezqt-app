# ///////////////////////////////////////////////////////////////
# KERNEL - Compatibility facade
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Backward-compatibility facade re-exporting all public symbols from services.

All imports from ``ezqt_app.kernel`` continue to work while the underlying
implementation lives in ``services/``.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path
from typing import Any

# Local imports — services re-exports
from ..services.application.app_service import AppService as Kernel
from ..services.application.app_service import AppService as _AppService
from ..services.application.assets_service import AssetsService as AssetsManager
from ..services.application.file_service import FileService as FileMaker
from ..services.application.resource_service import ResourceService as ResourceManager
from ..services.application.settings_loader import SettingsLoader as SettingsManager
from ..services.bootstrap import (
    InitializationSequence,
    Initializer,
    InitStep,
    StartupConfig,
    StepStatus,
    configure_startup,
    generate_assets,
    init,
    setup_project,
)
from ..services.config.config_service import get_config_service as _cs
from ..services.config.config_service import get_config_service as get_config_manager
from ..services.config.config_service import (
    get_package_resource,
    get_package_resource_content,
)
from ..services.settings import SettingsService, get_settings_service
from ..services.translation import (
    TranslationManager,
    change_language,
    get_available_languages,
    get_current_language,
    get_translation_manager,
    register_tr,
    set_tr,
    tr,
    translation_manager,
    unregister_tr,
)
from ..services.ui import (
    Fonts,
    MenuService,
    PanelService,
    SizePolicy,
    ThemeService,
    UiDefinitionsService,
    UIFunctions,
    WindowService,
)
from ..shared.resources import Icons, Images
from ..utils.runtime_paths import APP_PATH
from ..widgets.ui_main import Ui_MainWindow


# ///////////////////////////////////////////////////////////////
# APP FUNCTIONS HELPERS (inlined from kernel/app_functions/)
# ///////////////////////////////////////////////////////////////
def load_config(config_name: str) -> dict:
    """Load a named YAML configuration."""
    return _cs().load_config(config_name)


def get_config_value(config_name: str, key_path: str, default=None):
    """Get a single value from a named config by dot-separated key path."""
    return _cs().get_config_value(config_name, key_path, default)


def save_config(config_name: str, config_data: dict) -> None:
    """Persist a named configuration to its YAML file."""
    _cs().save_config(config_name, config_data)


def load_config_section(section: str) -> dict[str, Any]:
    """Load a YAML config section."""
    return _AppService.load_config(section)


def save_config_section(section: str, data: dict[str, Any]) -> bool:
    """Save a YAML config section."""
    try:
        _AppService.save_config(section, data)
        return True
    except Exception:
        return False


def get_setting(section: str, key: str, default: Any = None) -> Any:
    """Get a setting value by section and dot-separated key path."""
    try:
        config = load_config_section(section)
        keys = key.split(".")
        value = config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value
    except Exception:
        return default


def set_setting(section: str, key: str, value: Any) -> bool:
    """Write a setting value into a YAML config."""
    try:
        _AppService.write_yaml_config([section] + key.split("."), value)
        return True
    except Exception:
        return False


def load_fonts() -> bool:
    """Load bundled font resources."""
    try:
        ResourceManager.load_fonts_resources()
        return True
    except Exception:
        return False


def verify_assets() -> dict[str, bool]:
    """Verify presence of project assets (stub — no equivalent in v5)."""
    return {}


def get_resource_path(resource_type: str, name: str) -> Path | None:  # noqa: ARG001
    """Get a resource file path (stub — no equivalent in v5)."""
    return None


def get_kernel_instance() -> _AppService:
    """Return an AppService instance."""
    return _AppService()


def is_development_mode() -> bool:
    """Return True if the app is running in development mode."""
    try:
        return get_setting("app", "development_mode", False)
    except Exception:
        return False


def get_app_version() -> str:
    """Return the configured application version."""
    try:
        return get_setting("app", "version", "1.0.0")
    except Exception:
        return "1.0.0"


def get_app_name() -> str:
    """Return the configured application name."""
    try:
        return get_setting("app", "name", "EzQt App")
    except Exception:
        return "EzQt App"


# ///////////////////////////////////////////////////////////////
# UI FUNCTIONS HELPERS (inlined from kernel/ui_functions/)
# ///////////////////////////////////////////////////////////////
def maximize_window(window) -> None:
    """Maximize or restore the window depending on current state."""
    WindowService.maximize_restore(window)


def restore_window(window) -> None:
    """Restore window state when currently maximized."""
    if WindowService.get_status():
        WindowService.maximize_restore(window)


def toggle_window_state(window) -> None:
    """Toggle the main window state."""
    WindowService.maximize_restore(window)


def load_theme(window, custom_theme_file: str | None = None) -> None:
    """Load and apply theme on a window."""
    ThemeService.apply_theme(window, custom_theme_file)


def apply_theme(window, custom_theme_file: str | None = None) -> None:
    """Apply theme on a window."""
    ThemeService.apply_theme(window, custom_theme_file)


def apply_default_theme(window) -> None:
    """Apply default theme on a window."""
    ThemeService.apply_theme(window)


def animate_panel(window, panel: str, enable: bool = True) -> None:
    """Animate a panel by name ('menu' or 'settings')."""
    if panel == "menu":
        PanelService.toggle_menu_panel(window, enable)
        return
    if panel == "settings":
        PanelService.toggle_settings_panel(window, enable)


def select_menu_item(window, widget: str) -> None:
    """Mark a menu item as selected and deselect the others."""
    MenuService.deselect_menu(window, widget)
    MenuService.select_menu(window, widget)


def refresh_menu_style(widget) -> None:
    """Refresh style for a menu widget."""
    MenuService.refresh_style(widget)


def setup_custom_grips(window) -> None:
    """Configure custom grips and UI definitions."""
    UiDefinitionsService.apply_definitions(window)


def connect_window_events(window) -> None:
    """Connect core window UI events."""
    UiDefinitionsService.apply_definitions(window)


def setup_window_title_bar(window) -> None:
    """Configure window title bar behaviour."""
    UiDefinitionsService.apply_definitions(window)


def get_ui_functions_instance() -> UIFunctions:
    """Return a UIFunctions facade instance."""
    return UIFunctions()


def is_window_maximized() -> bool:
    """Return whether the main window is currently maximized."""
    return WindowService.get_status()


def get_window_status() -> bool:
    """Return current window maximize status."""
    return WindowService.get_status()


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    # Bootstrap
    "InitializationSequence",
    "Initializer",
    "InitStep",
    "StartupConfig",
    "StepStatus",
    "configure_startup",
    "generate_assets",
    "init",
    "setup_project",
    # Settings
    "SettingsService",
    "get_settings_service",
    # Translation
    "TranslationManager",
    "change_language",
    "get_available_languages",
    "get_current_language",
    "get_translation_manager",
    "register_tr",
    "set_tr",
    "tr",
    "translation_manager",
    "unregister_tr",
    # UI resources
    "Fonts",
    "SizePolicy",
    "Icons",
    "Images",
    # Paths
    "APP_PATH",
    # App functions — aliases
    "Kernel",
    "AssetsManager",
    "ResourceManager",
    "SettingsManager",
    "FileMaker",
    # App functions — config
    "get_config_manager",
    "load_config",
    "get_config_value",
    "save_config",
    "get_package_resource",
    "get_package_resource_content",
    # App functions — helpers
    "load_config_section",
    "save_config_section",
    "get_setting",
    "set_setting",
    "load_fonts",
    "verify_assets",
    "get_resource_path",
    "get_kernel_instance",
    "is_development_mode",
    "get_app_version",
    "get_app_name",
    # UI functions
    "UIFunctions",
    "Ui_MainWindow",
    "maximize_window",
    "restore_window",
    "toggle_window_state",
    "load_theme",
    "apply_theme",
    "apply_default_theme",
    "animate_panel",
    "select_menu_item",
    "refresh_menu_style",
    "setup_custom_grips",
    "connect_window_events",
    "setup_window_title_bar",
    "get_ui_functions_instance",
    "is_window_maximized",
    "get_window_status",
]
