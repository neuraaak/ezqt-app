# ///////////////////////////////////////////////////////////////
# APP_UTILS - Application utility functions
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////
"""
Utility functions for managing application data directories and configuration files.
Migrated from cli/runner.py.
"""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path

# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////


def get_app_data_dir() -> Path:
    """Get the application data directory."""
    return Path.home() / ".ezqt_app" / "data"


def ensure_data_dir() -> Path:
    """Ensure the data directory exists."""
    data_dir = get_app_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_config_file() -> Path:
    """Get the configuration file path."""
    data_dir = ensure_data_dir()
    return data_dir / "config.yaml"
