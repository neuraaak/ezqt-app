# ///////////////////////////////////////////////////////////////
# SERVICES.UI.COMPONENT_FACTORY - UI component factory service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Service implementation for reusable UI components."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
from ...domain.models.ui import FONT_SPECS, SIZE_POLICY_SPECS, FontSpec, SizePolicySpec
from ...domain.ports.ui_component_factory import UiComponentFactoryProtocol


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class UiComponentFactory(UiComponentFactoryProtocol):
    """Factory that exposes predefined UI component specifications."""

    def __init__(self) -> None:
        """Initialize the factory."""
        self._initialized = False

    def initialize(self) -> None:
        """Mark the factory as initialized (specs are statically defined)."""
        self._initialized = True

    def get_font(self, name: str) -> FontSpec | None:
        """Return a predefined font specification by name."""
        return FONT_SPECS.get(name)

    def get_size_policy(self, name: str) -> SizePolicySpec | None:
        """Return a predefined size policy specification by name."""
        return SIZE_POLICY_SPECS.get(name)


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
