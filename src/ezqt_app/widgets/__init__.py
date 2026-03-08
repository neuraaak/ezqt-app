# ///////////////////////////////////////////////////////////////
# WIDGETS - Widget package
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Widget package for EzQt_App — core and extended UI components."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports — core widgets
from .core import BottomBar, EzApplication, Header, Menu, PageContainer, SettingsPanel

# Local imports — custom grips
from .custom_grips import CustomGrip

# Local imports — extended widgets
from .extended import (
    MenuButton,
    SettingCheckbox,
    SettingSelect,
    SettingSlider,
    SettingText,
    SettingToggle,
    ThemeIcon,
)

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    # Core
    "BottomBar",
    "EzApplication",
    "Header",
    "Menu",
    "PageContainer",
    "SettingsPanel",
    # Custom grips
    "CustomGrip",
    # Extended
    "MenuButton",
    "SettingCheckbox",
    "SettingSelect",
    "SettingSlider",
    "SettingText",
    "SettingToggle",
    "ThemeIcon",
]
