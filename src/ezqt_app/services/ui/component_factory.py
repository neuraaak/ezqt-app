# ///////////////////////////////////////////////////////////////
# SERVICES.UI.COMPONENT_FACTORY - UI component factory service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Service implementation for reusable UI components."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy

# Local imports
from ...domain.models.ui import FONT_SPECS, SIZE_POLICY_SPECS
from ...domain.ports.ui_component_factory import UiComponentFactoryProtocol


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class UiComponentFactory(UiComponentFactoryProtocol):
    """Factory that creates and caches predefined UI components."""

    def __init__(self) -> None:
        """Initialize the factory cache."""
        self._fonts: dict[str, QFont] = {}
        self._size_policies: dict[str, QSizePolicy] = {}
        self._initialized = False

    def initialize(self) -> None:
        """Initialize all predefined fonts and size policies."""
        if self._initialized:
            return

        for name, spec in FONT_SPECS.items():
            font = QFont()
            font.setFamily(spec.family)
            font.setPointSize(spec.point_size)
            font.setBold(spec.bold)
            font.setItalic(spec.italic)
            self._fonts[name] = font

        for name, spec in SIZE_POLICY_SPECS.items():
            horizontal_policy = getattr(QSizePolicy.Policy, spec.horizontal_policy)
            vertical_policy = getattr(QSizePolicy.Policy, spec.vertical_policy)
            size_policy = QSizePolicy(horizontal_policy, vertical_policy)
            size_policy.setHorizontalStretch(spec.horizontal_stretch)
            size_policy.setVerticalStretch(spec.vertical_stretch)
            self._size_policies[name] = size_policy

        self._initialized = True

    def get_font(self, name: str) -> QFont | None:
        """Return a predefined font by name."""
        return self._fonts.get(name)

    def get_size_policy(self, name: str) -> QSizePolicy | None:
        """Return a predefined size policy by name."""
        return self._size_policies.get(name)


# ///////////////////////////////////////////////////////////////
# SINGLETONS
# ///////////////////////////////////////////////////////////////
_ui_component_factory = UiComponentFactory()


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_ui_component_factory() -> UiComponentFactory:
    """Return the singleton UI component factory."""
    return _ui_component_factory


# ///////////////////////////////////////////////////////////////
# LEGACY COMPATIBILITY REGISTRIES
# ///////////////////////////////////////////////////////////////
class Fonts:
    """Font registry populated by ``UiComponentFactory``."""

    SEGOE_UI_8_REG: QFont | None = None
    SEGOE_UI_10_REG: QFont | None = None
    SEGOE_UI_12_REG: QFont | None = None
    SEGOE_UI_8_SB: QFont | None = None
    SEGOE_UI_10_SB: QFont | None = None
    SEGOE_UI_12_SB: QFont | None = None

    @classmethod
    def initFonts(cls) -> None:
        """Initialize and map font constants from the factory."""
        factory = get_ui_component_factory()
        factory.initialize()

        cls.SEGOE_UI_8_REG = factory.get_font("SEGOE_UI_8_REG")
        cls.SEGOE_UI_10_REG = factory.get_font("SEGOE_UI_10_REG")
        cls.SEGOE_UI_12_REG = factory.get_font("SEGOE_UI_12_REG")
        cls.SEGOE_UI_8_SB = factory.get_font("SEGOE_UI_8_SB")
        cls.SEGOE_UI_10_SB = factory.get_font("SEGOE_UI_10_SB")
        cls.SEGOE_UI_12_SB = factory.get_font("SEGOE_UI_12_SB")


class SizePolicy:
    """Size policy registry populated by ``UiComponentFactory``."""

    H_EXPANDING_V_FIXED: QSizePolicy | None = None
    H_EXPANDING_V_PREFERRED: QSizePolicy | None = None
    H_PREFERRED_V_EXPANDING: QSizePolicy | None = None
    H_EXPANDING_V_EXPANDING: QSizePolicy | None = None

    @classmethod
    def initSizePolicy(cls) -> None:
        """Initialize and map size policy constants from the factory."""
        factory = get_ui_component_factory()
        factory.initialize()

        cls.H_EXPANDING_V_FIXED = factory.get_size_policy("H_EXPANDING_V_FIXED")
        cls.H_EXPANDING_V_PREFERRED = factory.get_size_policy("H_EXPANDING_V_PREFERRED")
        cls.H_PREFERRED_V_EXPANDING = factory.get_size_policy("H_PREFERRED_V_EXPANDING")
        cls.H_EXPANDING_V_EXPANDING = factory.get_size_policy("H_EXPANDING_V_EXPANDING")
