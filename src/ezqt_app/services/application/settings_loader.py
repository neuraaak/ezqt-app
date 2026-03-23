# ///////////////////////////////////////////////////////////////
# SERVICES.APPLICATION.SETTINGS_LOADER - Settings loader service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Loads application settings from YAML and applies them to SettingsService."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import re
from pathlib import Path
from typing import Any

# Third-party imports
import yaml
from ezpl import Ezpl

from ...utils.printer import get_printer, set_global_debug

# Local imports
from ..config.config_service import get_config_service
from ..settings import get_settings_service

# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////
_DEFAULT_USER_DIR = Path.home() / ".ezqt"
_DEFAULT_LOGS_DIR = _DEFAULT_USER_DIR / "logs"


def _build_log_file_path(
    app_name: str | None = None,
    logs_dir: str | Path | None = None,
    log_file_name: str | None = None,
) -> Path:
    """Build the absolute log file path from app identity and optional overrides."""
    resolved_logs_dir = (
        Path(logs_dir).expanduser() if logs_dir is not None else _DEFAULT_LOGS_DIR
    )
    if log_file_name and log_file_name.strip():
        file_name = log_file_name.strip()
    else:
        stem = re.sub(
            r"[^a-zA-Z0-9._-]+", "_", (app_name or "ezqt_app").strip().lower()
        )
        stem = stem.strip("._-") or "ezqt_app"
        file_name = f"{stem}.log"
    file_path = resolved_logs_dir / file_name
    if file_path.suffix == "":
        file_path = file_path.with_suffix(".log")
    return file_path.resolve()


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class SettingsLoader:
    """Loads ``app.config.yaml`` and populates the settings service.

    Reads the YAML configuration file, extracts application and GUI
    parameters, and injects them into the singleton ``SettingsService``.
    """

    # -----------------------------------------------------------
    # Static API
    # -----------------------------------------------------------

    @staticmethod
    def load_app_settings(
        yaml_file: Path | None = None,
        logs_dir_override: str | Path | None = None,
        log_file_name_override: str | None = None,
    ) -> dict:
        """Load application settings from YAML and apply to SettingsService.

        Parameters
        ----------
        yaml_file:
            Path to the YAML file. Defaults to the package ``app.config.yaml``.

        Returns
        -------
        dict
            Raw ``app`` section from the YAML file.
        """
        if yaml_file is None:
            data = get_config_service().load_config("app", force_reload=True)
            app_data = data.get("app", {})
        else:
            with open(yaml_file, encoding="utf-8") as file:
                data = yaml.safe_load(file)
                app_data = data.get("app", {})

        settings_service = get_settings_service()
        app_name = str(app_data.get("name", "ezqt_app"))
        logging_cfg: dict[str, Any] = (
            app_data.get("logging", {})
            if isinstance(app_data.get("logging", {}), dict)
            else {}
        )

        config_logs_dir = app_data.get("logs_dir") or logging_cfg.get("dir")
        config_log_file_name = app_data.get("log_file_name") or logging_cfg.get(
            "file_name"
        )

        resolved_log_file = _build_log_file_path(
            app_name=app_name,
            logs_dir=logs_dir_override or config_logs_dir,
            log_file_name=log_file_name_override or config_log_file_name,
        )
        resolved_log_file.parent.mkdir(parents=True, exist_ok=True)
        if Ezpl.is_initialized():
            Ezpl().set_log_file(resolved_log_file)
        else:
            Ezpl(log_file=resolved_log_file)

        debug_enabled = bool(app_data.get("debug", False))

        # App identity
        settings_service.set_app_name(app_data["name"])
        settings_service.set_app_description(app_data["description"])
        settings_service.set_custom_title_bar_enabled(True)
        settings_service.set_debug_enabled(debug_enabled)
        set_global_debug(debug_enabled)

        # Window dimensions
        settings_service.set_app_min_size(
            width=app_data["app_min_width"],
            height=app_data["app_min_height"],
        )
        settings_service.set_app_dimensions(
            width=app_data["app_width"],
            height=app_data["app_height"],
        )

        # GUI settings
        try:
            settings_panel = data.get("settings_panel", {})
            settings_service.set_theme(
                settings_panel.get("theme", {}).get("default", app_data["theme"])
            )
        except KeyError:
            settings_service.set_theme(app_data["theme"])

        settings_service.set_menu_widths(
            shrinked=app_data["menu_panel_shrinked_width"],
            extended=app_data["menu_panel_extended_width"],
        )
        settings_service.set_settings_panel_width(app_data["settings_panel_width"])
        settings_service.set_time_animation(app_data["time_animation"])

        # Display summary through the globally configured printer instance.
        get_printer().config_display(app_data)

        return app_data
