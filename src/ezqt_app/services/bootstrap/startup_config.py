# ///////////////////////////////////////////////////////////////
# SERVICES.BOOTSTRAP.STARTUP_CONFIG - System startup configuration
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""System-level startup configuration — encoding, locale, env vars, project root."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import contextlib
import locale
import os
import sys


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class StartupConfig:
    """Manages system-level startup configuration.

    Handles encoding, locale, environment variables and project root
    detection.  Idempotent: subsequent calls to :meth:`configure` are
    no-ops once the instance is configured.
    """

    def __init__(self) -> None:
        self._configured = False

    def configure(self) -> None:
        """Run all startup configuration steps (idempotent)."""
        if self._configured:
            return

        self._configure_encoding()
        self._configure_environment()
        self._configure_locale()
        self._configure_system()
        self._configure_project_root()

        self._configured = True

    # ------------------------------------------------------------------
    # Configuration steps
    # ------------------------------------------------------------------

    def _configure_encoding(self) -> None:
        """Force UTF-8 encoding on stdout/stderr."""
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

    def _configure_environment(self) -> None:
        """Set mandatory Qt/Python environment variables."""
        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["QT_FONT_DPI"] = "96"
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"

    def _configure_locale(self) -> None:
        """Set locale to the system default (UTF-8 preferred)."""
        with contextlib.suppress(locale.Error):
            locale.setlocale(locale.LC_ALL, "")

    def _configure_system(self) -> None:
        """Apply platform-specific Qt environment variables."""
        if sys.platform.startswith("win"):
            self._configure_windows()
        elif sys.platform.startswith("linux"):
            self._configure_linux()
        elif sys.platform.startswith("darwin"):
            self._configure_macos()

    def _configure_windows(self) -> None:
        os.environ["QT_QPA_PLATFORM"] = "windows:dpiawareness=0"

    def _configure_linux(self) -> None:
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    def _configure_macos(self) -> None:
        os.environ["QT_QPA_PLATFORM"] = "cocoa"

    def _configure_project_root(self) -> None:
        """Detect and register the project root with the config service."""
        from pathlib import Path

        from ..application.app_service import AppService

        project_root = Path.cwd()

        # If running from bin/, go up one level
        if project_root.name == "bin" and (project_root.parent / "main.py").exists():
            project_root = project_root.parent
        elif (project_root / "main.py").exists():
            pass  # Already at project root
        else:
            # Walk up looking for a main.py
            current = project_root
            while current.parent != current:
                if (current.parent / "main.py").exists():
                    project_root = current.parent
                    break
                current = current.parent

        AppService.set_project_root(project_root)

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def get_encoding(self) -> str:
        return getattr(sys.stdout, "encoding", "utf-8")

    def get_locale(self) -> str | None:
        try:
            return locale.getlocale()[0]
        except (locale.Error, IndexError):
            return None

    def is_configured(self) -> bool:
        return self._configured

    def reset(self) -> None:
        self._configured = False
