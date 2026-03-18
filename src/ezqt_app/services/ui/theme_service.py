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
    def apply_theme(window: MainWindowProtocol) -> None:
        """Load all QSS files from the themes directory and apply the merged stylesheet.

        All ``.qss`` files found under ``<app_root>/bin/themes/`` are loaded in
        alphabetical order and concatenated before palette variables are resolved.
        When that directory is absent or empty, the package's own
        ``resources/themes/`` directory is used as fallback.

        Args:
            window: The application window whose ``ui.styleSheet`` will be
                updated.  Must expose ``window.ui.styleSheet.setStyleSheet``.
        """
        settings_service = get_settings_service()
        config_service = get_config_service()

        theme_preset = settings_service.gui.THEME_PRESET
        theme_variant = settings_service.gui.THEME
        theme_config = config_service.load_config("theme")
        palette = theme_config.get("palette", {})
        colors: dict[str, str] = palette.get(theme_preset, {}).get(theme_variant, {})

        merged_style = ThemeService._load_themes_content()
        merged_style = ThemeService._resolve_variables(merged_style, colors)

        window.ui.style_sheet.setStyleSheet(f"{merged_style}\n")

    @staticmethod
    def get_available_themes() -> list[tuple[str, str]]:
        """Return available theme options as ``(display_label, internal_value)`` pairs.

        Reads ``palette`` keys from ``theme.config.yaml`` and generates one entry
        per ``preset × variant`` combination, e.g.
        ``("Blue Gray - Dark", "blue_gray:dark")``.

        Returns:
            List of ``(display_label, internal_value)`` tuples, one per theme variant.
        """
        config_service = get_config_service()
        theme_config = config_service.load_config("theme")
        palette = theme_config.get("palette", {})

        options: list[tuple[str, str]] = []
        for preset_key, variants in palette.items():
            if not isinstance(variants, dict):
                continue
            display_preset = preset_key.replace("-", " ").title()
            for variant_key in variants:
                label = f"{display_preset} - {variant_key.title()}"
                options.append((label, f"{preset_key}:{variant_key}"))
        return options

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
    def _load_themes_content() -> str:
        """Load and merge all QSS files from the themes directory.

        All ``.qss`` files are loaded in alphabetical order and joined with a
        blank line separator so that rules from multiple files are concatenated
        into a single stylesheet string.

        Resolution order:
        1. ``<app_root>/bin/themes/`` — project-local files (includes lib
           defaults copied during initialisation and any developer additions).
        2. Package ``resources/themes/`` — fallback when the local directory is
           absent or contains no ``.qss`` files.

        ``qtstrap.qss`` is excluded in both locations.

        Returns:
            Merged stylesheet content ready for variable resolution.

        Raises:
            FileNotFoundError: When no ``.qss`` files are found in either location.
        """
        _EXCLUDED = {"qtstrap.qss"}

        local_themes_dir = APP_PATH / "bin" / "themes"
        local_files = (
            sorted(f for f in local_themes_dir.glob("*.qss") if f.name not in _EXCLUDED)
            if local_themes_dir.is_dir()
            else []
        )

        if local_files:
            return "\n\n".join(f.read_text(encoding="utf-8") for f in local_files)

        package_themes_dir = (
            Path(__file__).resolve().parents[2] / "resources" / "themes"
        )
        package_files = (
            sorted(
                f for f in package_themes_dir.glob("*.qss") if f.name not in _EXCLUDED
            )
            if package_themes_dir.is_dir()
            else []
        )

        if package_files:
            return "\n\n".join(f.read_text(encoding="utf-8") for f in package_files)

        raise FileNotFoundError(
            "No theme files found in local (bin/themes/) or package resources."
        )
