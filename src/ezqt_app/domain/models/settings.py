# ///////////////////////////////////////////////////////////////
# DOMAIN.MODELS.SETTINGS - Settings state models
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Pure domain models for mutable application settings state."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from dataclasses import dataclass, field


# ///////////////////////////////////////////////////////////////
# DATACLASSES
# ///////////////////////////////////////////////////////////////
@dataclass(slots=True)
class AppSettingsModel:
    """Mutable application settings values."""

    NAME: str = "MyApplication"
    DESCRIPTION: str = "MyDescription"
    ENABLE_CUSTOM_TITLE_BAR: bool = True
    APP_MIN_SIZE: tuple[int, int] = (940, 560)
    APP_WIDTH: int = 1280
    APP_HEIGHT: int = 720
    DEBUG: bool = False


@dataclass(slots=True)
class GuiSettingsModel:
    """Mutable GUI settings values."""

    THEME: str = "dark"
    MENU_PANEL_SHRINKED_WIDTH: int = 60
    MENU_PANEL_EXTENDED_WIDTH: int = 240
    SETTINGS_PANEL_WIDTH: int = 240
    TIME_ANIMATION: int = 400


@dataclass(slots=True)
class SettingsStateModel:
    """Mutable aggregate application settings state."""

    app: AppSettingsModel = field(default_factory=AppSettingsModel)
    gui: GuiSettingsModel = field(default_factory=GuiSettingsModel)
