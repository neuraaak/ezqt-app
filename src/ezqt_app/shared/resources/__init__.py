# ///////////////////////////////////////////////////////////////
# SHARED.RESOURCES - Shared resource definitions
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Shared static resource path definitions."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

# Local imports
from ...resources import base_resources_rc  # type: ignore # noqa: F401
from ...utils.runtime_paths import APP_PATH
from .icons import Icons as _PackageIcons
from .images import Images as _PackageImages

Icons = _PackageIcons
Images = _PackageImages


def _load_module_from_file(module_name: str, file_path: Path) -> ModuleType | None:
    """Import a Python module directly from file when it exists."""
    if not file_path.exists() or not file_path.is_file():
        return None

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None

    sys.modules[module_name] = module
    return module


# Register user-generated Qt resources (bin/resources_rc.py) without
# replacing packaged fallback icons/images.
_load_module_from_file(
    "ezqt_app._runtime_resources_rc", APP_PATH / "bin" / "resources_rc.py"
)

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["Icons", "Images"]
