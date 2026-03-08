"""
Theme service implementation for UI styling.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path
from typing import Any

# Local imports
from ...utils.runtime_paths import APP_PATH
from ..config import get_config_service
from ..settings import get_settings_service


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ThemeService:
    """Service responsible for loading and applying QSS themes."""

    @staticmethod
    def apply_theme(window: Any, custom_theme_file: str | None = None) -> None:
        """Load and apply either a custom QSS file or the default package theme."""
        settings_service = get_settings_service()
        config_service = get_config_service()

        theme_name = settings_service.gui.THEME
        theme_config = config_service.load_config("theme")
        colors = theme_config.get("palette", {}).get(theme_name, {})

        main_style = ThemeService._load_theme_content(custom_theme_file)

        for key, color in colors.items():
            main_style = main_style.replace(key, color)

        window.ui.styleSheet.setStyleSheet(f"{main_style}\n")

    @staticmethod
    def _load_theme_content(custom_theme_file: str | None) -> str:
        """Resolve and read theme stylesheet content from local or package paths."""
        if custom_theme_file:
            custom_qss = APP_PATH / "bin" / "themes" / custom_theme_file
            if custom_qss.exists():
                return custom_qss.read_text(encoding="utf-8")
            raise FileNotFoundError(f"Custom theme file not found: {custom_qss}")

        local_qss = APP_PATH / "bin" / "themes" / "main_theme.qss"
        if local_qss.exists():
            return local_qss.read_text(encoding="utf-8")

        package_qss = (
            Path(__file__).resolve().parents[2]
            / "resources"
            / "themes"
            / "main_theme.qss"
        )
        if package_qss.exists():
            return package_qss.read_text(encoding="utf-8")

        raise FileNotFoundError(
            "Default theme file not found in local or package resources."
        )
