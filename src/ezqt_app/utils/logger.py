# ///////////////////////////////////////////////////////////////
# UTILS.LOGGER - File logging utility based on ezpl
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Centralized file logger utility built on top of ezpl."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import re
from pathlib import Path
from typing import Any

# Third-party imports
from ezpl import Ezpl

# Local imports


# ///////////////////////////////////////////////////////////////
# CONSTANTS
# ///////////////////////////////////////////////////////////////
DEFAULT_USER_DIR = Path.home() / ".ezqt"
DEFAULT_LOGS_DIR = DEFAULT_USER_DIR / "logs"
DEFAULT_LOG_FILE_NAME = "ezqt_app.log"


# ///////////////////////////////////////////////////////////////
# HELPERS
# ///////////////////////////////////////////////////////////////
def _sanitize_log_stem(name: str) -> str:
    """Return a filesystem-safe stem from an application name."""
    stem = re.sub(r"[^a-zA-Z0-9._-]+", "_", name.strip().lower())
    return stem.strip("._-") or "ezqt_app"


def build_log_file_path(
    app_name: str | None = None,
    logs_dir: str | Path | None = None,
    log_file_name: str | None = None,
) -> Path:
    """Build the absolute log file path from app identity and optional overrides."""
    resolved_logs_dir = (
        Path(logs_dir).expanduser() if logs_dir is not None else DEFAULT_LOGS_DIR
    )

    if log_file_name and log_file_name.strip():
        file_name = log_file_name.strip()
    else:
        stem = _sanitize_log_stem(app_name or "ezqt_app")
        file_name = f"{stem}.log"

    file_path = resolved_logs_dir / file_name
    if file_path.suffix == "":
        file_path = file_path.with_suffix(".log")

    return file_path.resolve()


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class Logger:
    """Centralized logger with a minimal API similar to ``Printer``.

    This wrapper uses ``ezpl`` for file logging and keeps configuration simple:
    - Default log file: ``~/.ezqt/logs/<app_name>.log``
    - Default level: ``INFO``
    - ``verbose=True`` enables ``verbose_msg`` forwarding to ``debug``
    """

    def __init__(
        self,
        verbose: bool = False,
        log_file: Path | None = None,
        level: str = "INFO",
    ) -> None:
        self.verbose = verbose
        requested_log_file = (
            log_file.resolve()
            if log_file is not None
            else build_log_file_path(app_name="ezqt_app")
        )
        requested_log_file.parent.mkdir(parents=True, exist_ok=True)

        if Ezpl.is_initialized():
            ezpl = Ezpl()
        else:
            ezpl = Ezpl(
                log_file=requested_log_file,
                file_logger_level=level.upper(),
            )

        self._logger = ezpl.get_logger()
        active_log_file = getattr(self._logger, "_log_file", requested_log_file)
        self._log_file = Path(active_log_file)
        self._logger.set_level(level.upper())

    @property
    def level(self) -> str:
        """Return the active logger level."""
        return self._logger.level

    def set_level(self, level: str) -> None:
        """Set the logger level."""
        self._logger.set_level(level.upper())

    def get_log_file(self) -> Path:
        """Return the configured log file path."""
        return self._log_file

    def debug(self, message: Any) -> None:
        """Log a debug message."""
        self._logger.debug(message)

    def info(self, message: Any) -> None:
        """Log an info message."""
        self._logger.info(message)

    def success(self, message: Any) -> None:
        """Log a success message."""
        self._logger.success(message)

    def warning(self, message: Any) -> None:
        """Log a warning message."""
        self._logger.warning(message)

    def error(self, message: Any) -> None:
        """Log an error message."""
        self._logger.error(message)

    def critical(self, message: Any) -> None:
        """Log a critical message."""
        self._logger.critical(message)

    def exception(self, message: Any) -> None:
        """Log an exception message with traceback."""
        self._logger.exception(message)

    def verbose_msg(self, message: Any) -> None:
        """Log a debug message only when verbose mode is enabled."""
        if self.verbose:
            self._logger.debug(message)


# ///////////////////////////////////////////////////////////////
# SINGLETONS
# ///////////////////////////////////////////////////////////////
_default_logger: Logger | None = None


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_logger(
    verbose: bool = False,
    log_file: Path | None = None,
    level: str = "INFO",
) -> Logger:
    """Return a logger instance, creating a dedicated one if options differ."""
    global _default_logger

    if _default_logger is None:
        _default_logger = Logger(verbose=verbose, log_file=log_file, level=level)
        return _default_logger

    _default_logger.verbose = verbose
    if level.upper() != _default_logger.level:
        _default_logger.set_level(level)

    if log_file is not None and log_file.resolve() != _default_logger.get_log_file():
        _default_logger.warning(
            "Logger already initialized with another log file; keeping current file."
        )

    return _default_logger


def set_global_log_file(
    log_file: Path,
    level: str = "INFO",
    verbose: bool = False,
) -> Logger:
    """Initialize the default logger with an explicit global log file path."""
    global _default_logger

    resolved = log_file.resolve()
    if _default_logger is None:
        _default_logger = Logger(verbose=verbose, log_file=resolved, level=level)
        return _default_logger

    if resolved != _default_logger.get_log_file():
        _default_logger.warning(
            "Logger already initialized with another log file; keeping current file."
        )
    if level.upper() != _default_logger.level:
        _default_logger.set_level(level)
    _default_logger.verbose = verbose
    return _default_logger


def set_global_log_level(level: str) -> None:
    """Set the level of the default logger instance."""
    get_logger().set_level(level)
