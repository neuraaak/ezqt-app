# ///////////////////////////////////////////////////////////////
# UTILS.DIAGNOSTICS - Unified warning helpers
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Helpers to standardize logger/printer warning outputs."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
from .logger import get_logger
from .printer import get_printer


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def _format_log_message(code: str, message: str, error: Exception | None = None) -> str:
    """Build a codified warning line for file logs."""
    if error is None:
        return f"[{code}] {message}"
    return f"[{code}] {message}: {error}"


def warn_tech(code: str, message: str, error: Exception | None = None) -> None:
    """Log a technical warning (logger only, no console output)."""
    get_logger().warning(_format_log_message(code=code, message=message, error=error))


def warn_user(
    code: str,
    user_message: str,
    *,
    log_message: str | None = None,
    error: Exception | None = None,
    show_error_details_in_verbose: bool = True,
) -> None:
    """Emit a user-facing warning and a codified log warning.

    Console output should stay concise and readable for end users,
    while logs keep technical details and stable error codes.
    """
    get_logger().warning(
        _format_log_message(
            code=code,
            message=log_message or user_message,
            error=error,
        )
    )
    get_printer().warning(user_message)

    if error is not None and show_error_details_in_verbose:
        get_printer().verbose_msg(f"[{code}] {type(error).__name__}: {error}")


def info_user(message: str) -> None:
    """Emit a user-facing informational message (console only)."""
    get_printer().info(message)
