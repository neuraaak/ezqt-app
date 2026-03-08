# ///////////////////////////////////////////////////////////////
# DOMAIN.PORTS.CONFIG_SERVICE - Config service port
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Protocol definitions for configuration services."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path
from typing import Any, Protocol


# ///////////////////////////////////////////////////////////////
# PROTOCOLS
# ///////////////////////////////////////////////////////////////
class ConfigServiceProtocol(Protocol):
    """Technical contract for configuration services."""

    def set_project_root(self, project_root: Path | str) -> None:
        """Set the active project root directory."""

    def load_config(
        self, config_name: str, force_reload: bool = False
    ) -> dict[str, Any]:
        """Load a named configuration."""

    def get_config_value(
        self, config_name: str, key_path: str, default: Any = None
    ) -> Any:
        """Read a specific value from a configuration."""

    def save_config(self, config_name: str, config_data: dict[str, Any]) -> bool:
        """Persist a named configuration."""
