# ///////////////////////////////////////////////////////////////
# DOMAIN.MODELS.UI - UI component specifications
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Pure domain specifications for UI component factories."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from dataclasses import dataclass


# ///////////////////////////////////////////////////////////////
# DATACLASSES
# ///////////////////////////////////////////////////////////////
@dataclass(frozen=True)
class FontSpec:
    """Immutable specification for a ``QFont`` instance."""

    family: str
    point_size: int
    bold: bool = False
    italic: bool = False


@dataclass(frozen=True)
class SizePolicySpec:
    """Immutable specification for a ``QSizePolicy`` instance."""

    horizontal_policy: str
    vertical_policy: str
    horizontal_stretch: int = 0
    vertical_stretch: int = 0


# ///////////////////////////////////////////////////////////////
# SPECIFICATIONS
# ///////////////////////////////////////////////////////////////
FONT_SPECS: dict[str, FontSpec] = {
    "SEGOE_UI_8_REG": FontSpec(family="Segoe UI", point_size=8),
    "SEGOE_UI_10_REG": FontSpec(family="Segoe UI", point_size=10),
    "SEGOE_UI_12_REG": FontSpec(family="Segoe UI", point_size=12),
    "SEGOE_UI_8_SB": FontSpec(family="Segoe UI Semibold", point_size=8),
    "SEGOE_UI_10_SB": FontSpec(family="Segoe UI Semibold", point_size=10),
    "SEGOE_UI_12_SB": FontSpec(family="Segoe UI Semibold", point_size=12),
}

SIZE_POLICY_SPECS: dict[str, SizePolicySpec] = {
    "H_EXPANDING_V_FIXED": SizePolicySpec(
        horizontal_policy="Expanding",
        vertical_policy="Fixed",
    ),
    "H_EXPANDING_V_PREFERRED": SizePolicySpec(
        horizontal_policy="Expanding",
        vertical_policy="Preferred",
    ),
    "H_PREFERRED_V_EXPANDING": SizePolicySpec(
        horizontal_policy="Preferred",
        vertical_policy="Expanding",
    ),
    "H_EXPANDING_V_EXPANDING": SizePolicySpec(
        horizontal_policy="Expanding",
        vertical_policy="Expanding",
    ),
}
