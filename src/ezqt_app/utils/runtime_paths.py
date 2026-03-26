# ///////////////////////////////////////////////////////////////
# UTILS.RUNTIME_PATHS - Runtime path helpers
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

# ruff: noqa: I001

"""Low-level path helpers used at runtime."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import sys
from pathlib import Path
from typing import Final

# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////
APP_PATH: Final[Path] = Path(
    getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent)
)

# ///////////////////////////////////////////////////////////////
# MUTABLE BIN PATH
# ///////////////////////////////////////////////////////////////
_bin_path: Path | None = None
_bin_path_user_set: bool = False


def get_bin_path() -> Path:
    """Return the active bin directory.

    Defaults to ``APP_PATH / "bin"`` unless overridden by :func:`set_bin_path`.
    """
    return _bin_path if _bin_path is not None else APP_PATH / "bin"


def set_bin_path(path: Path) -> None:
    """Override the bin directory used by all runtime services.

    Call this during bootstrap (before any service loads resources) when the
    consuming application places its assets in a non-default folder.

    Args:
        path: Absolute path to the bin directory (e.g. ``project_root / "binaries"``).
    """
    global _bin_path, _bin_path_user_set  # noqa: PLW0603
    _bin_path = path
    _bin_path_user_set = True


def _sync_bin_path_from_root(path: Path) -> None:  # pyright: ignore[reportUnusedFunction]
    """Update bin path derived from the project root, unless user-set.

    Called internally by ``ConfigService.set_project_root()`` so that services
    relying on :func:`get_bin_path` stay in sync without going through bootstrap.
    No-op when the user has already called :func:`set_bin_path` explicitly.
    """
    global _bin_path  # noqa: PLW0603
    if not _bin_path_user_set:
        _bin_path = path
