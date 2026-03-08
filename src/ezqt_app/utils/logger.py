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
from pathlib import Path
from typing import Any

# Third-party imports
from ezpl import Ezpl

# Local imports
from .runtime_paths import APP_PATH


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class Logger:
    """Centralized logger with a minimal API similar to ``Printer``.

    This wrapper uses ``ezpl`` for file logging and keeps configuration simple:
    - Default log file: ``<APP_PATH>/logs/ezqt_app.log``
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
            log_file or (APP_PATH / "logs" / "ezqt_app.log")
        ).resolve()
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


def set_global_log_level(level: str) -> None:
    """Set the level of the default logger instance."""
    get_logger().set_level(level)
