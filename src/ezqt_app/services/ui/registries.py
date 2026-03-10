# ///////////////////////////////////////////////////////////////
# SERVICES.UI.REGISTRIES - Qt font and size-policy registries
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Legacy Qt registries for fonts and size policies.

These classes materialise ``FontSpec`` / ``SizePolicySpec`` domain objects
into live Qt objects and expose them as class-level attributes for use by
widget code.  They are populated by calling ``initFonts()`` /
``initSizePolicy()`` once during application startup.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy

# Local imports
from ...domain.models.ui import FontSpec, SizePolicySpec
from .component_factory import get_ui_component_factory


# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////
def _spec_to_qfont(spec: FontSpec) -> QFont:
    """Convert a ``FontSpec`` domain object to a ``QFont`` instance."""
    font = QFont()
    font.setFamily(spec.family)
    font.setPointSize(spec.point_size)
    font.setBold(spec.bold)
    font.setItalic(spec.italic)
    return font


def _spec_to_qsize_policy(spec: SizePolicySpec) -> QSizePolicy:
    """Convert a ``SizePolicySpec`` domain object to a ``QSizePolicy`` instance."""
    h_policy = getattr(QSizePolicy.Policy, spec.horizontal_policy)
    v_policy = getattr(QSizePolicy.Policy, spec.vertical_policy)
    size_policy = QSizePolicy(h_policy, v_policy)
    size_policy.setHorizontalStretch(spec.horizontal_stretch)
    size_policy.setVerticalStretch(spec.vertical_stretch)
    return size_policy


# ///////////////////////////////////////////////////////////////
# REGISTRIES
# ///////////////////////////////////////////////////////////////
class Fonts:
    """Font registry — populate by calling ``initFonts()`` at startup."""

    SEGOE_UI_8_REG: QFont | None = None
    SEGOE_UI_10_REG: QFont | None = None
    SEGOE_UI_12_REG: QFont | None = None
    SEGOE_UI_8_SB: QFont | None = None
    SEGOE_UI_10_SB: QFont | None = None
    SEGOE_UI_12_SB: QFont | None = None

    @classmethod
    def initFonts(cls) -> None:
        """Initialise font constants from the UI component factory."""
        factory = get_ui_component_factory()
        factory.initialize()

        for attr_name in (
            "SEGOE_UI_8_REG",
            "SEGOE_UI_10_REG",
            "SEGOE_UI_12_REG",
            "SEGOE_UI_8_SB",
            "SEGOE_UI_10_SB",
            "SEGOE_UI_12_SB",
        ):
            spec = factory.get_font(attr_name)
            if spec is not None:
                setattr(cls, attr_name, _spec_to_qfont(spec))


class SizePolicy:
    """Size-policy registry — populate by calling ``initSizePolicy()`` at startup."""

    H_EXPANDING_V_FIXED: QSizePolicy | None = None
    H_EXPANDING_V_PREFERRED: QSizePolicy | None = None
    H_PREFERRED_V_EXPANDING: QSizePolicy | None = None
    H_EXPANDING_V_EXPANDING: QSizePolicy | None = None

    @classmethod
    def initSizePolicy(cls) -> None:
        """Initialise size-policy constants from the UI component factory."""
        factory = get_ui_component_factory()
        factory.initialize()

        for attr_name in (
            "H_EXPANDING_V_FIXED",
            "H_EXPANDING_V_PREFERRED",
            "H_PREFERRED_V_EXPANDING",
            "H_EXPANDING_V_EXPANDING",
        ):
            spec = factory.get_size_policy(attr_name)
            if spec is not None:
                setattr(cls, attr_name, _spec_to_qsize_policy(spec))
