# ///////////////////////////////////////////////////////////////
# DOMAIN.MODELS.RUNTIME - Runtime state model
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Pure domain model for mutable runtime state."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from dataclasses import dataclass


# ///////////////////////////////////////////////////////////////
# DATACLASSES
# ///////////////////////////////////////////////////////////////
@dataclass(slots=True)
class RuntimeStateModel:
    """Mutable runtime state values used by runtime services."""

    app_initialized: bool = False
    app_running: bool = False
    debug_mode: bool = False
    verbose_mode: bool = False
    global_state: bool = False
    global_title_bar: bool = True
