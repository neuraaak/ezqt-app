"""
Theme service implementation for UI styling.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import re
from pathlib import Path

# Local imports
from ...domain.ports.main_window import MainWindowProtocol
from ...utils.runtime_paths import APP_PATH
from ..config import get_config_service
from ..settings import get_settings_service

# ///////////////////////////////////////////////////////////////
# VARIABLES
# ///////////////////////////////////////////////////////////////
# Matches var(--variable_name) references in QSS stylesheets.
_VAR_PATTERN: re.Pattern[str] = re.compile(r"var\(--([a-zA-Z0-9_]+)\)")


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ThemeService:
    """Service responsible for loading and applying QSS themes.

    Theme variables are declared without prefix in theme config files
    (e.g. ``main_surface``) and referenced in QSS files using the
    standard CSS custom property notation ``var(--variable_name)``.
    The service resolves each reference to its palette value before
    applying the stylesheet.
    """

    @staticmethod
    def apply_theme(
        window: MainWindowProtocol, custom_theme_file: str | None = None
    ) -> None:
        """Load and apply either a custom QSS file or the default package theme.

        Args:
            window: The application window whose ``ui.styleSheet`` will be
                updated.  Must expose ``window.ui.styleSheet.setStyleSheet``.
            custom_theme_file: Optional filename of a QSS file located under
                ``<app_root>/bin/themes/``.  When ``None`` the default package
                theme is used.
        """
        settings_service = get_settings_service()
        config_service = get_config_service()

        theme_name = settings_service.gui.THEME
        theme_config = config_service.load_config("theme")
        colors: dict[str, str] = theme_config.get("palette", {}).get(theme_name, {})

        main_style = ThemeService._load_theme_content(custom_theme_file)
        main_style = ThemeService._resolve_variables(main_style, colors)

        window.ui.style_sheet.setStyleSheet(f"{main_style}\n")

    @staticmethod
    def _resolve_variables(stylesheet: str, colors: dict[str, str]) -> str:
        """Replace all ``--var("name")`` tokens with their palette values.

        Each token ``var(--name)`` is substituted with the value found under
        the key ``name`` in *colors*.  Unrecognised variable names are left
        unchanged so that QSS parsing failures are easier to diagnose.

        Args:
            stylesheet: Raw QSS content containing ``var(--…)`` references.
            colors: Mapping of variable name to CSS value, as loaded from the
                active theme palette.

        Returns:
            The stylesheet with all resolvable variable references substituted.
        """

        def _replace(match: re.Match[str]) -> str:
            var_name = match.group(1)
            # Return the palette value when found; preserve the token otherwise.
            return colors.get(var_name, match.group(0))

        return _VAR_PATTERN.sub(_replace, stylesheet)

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
