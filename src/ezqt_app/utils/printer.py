# ///////////////////////////////////////////////////////////////
# UTILS.PRINTER - Console output utility
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Centralized console printer with consistent formatting and color support."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from colorama import Fore, Style


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class Printer:
    """Centralized printer for console output with consistent formatting.

    Provides methods for different message types:
    - Info messages (light gray)
    - Success messages (green)
    - Warning messages (yellow)
    - Error messages (red)
    - Verbose messages (light black, gated by ``verbose`` flag)
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def info(self, message: str, prefix: str = "~") -> None:
        """Print an info message."""
        print(f"{Fore.LIGHTBLACK_EX}{prefix} {message}{Style.RESET_ALL}")

    def success(self, message: str, prefix: str = "✓") -> None:
        """Print a success message."""
        print(f"{Fore.GREEN}{prefix} {message}{Style.RESET_ALL}")

    def warning(self, message: str, prefix: str = "!") -> None:
        """Print a warning message."""
        print(f"{Fore.YELLOW}{prefix} {message}{Style.RESET_ALL}")

    def error(self, message: str, prefix: str = "✗") -> None:
        """Print an error message."""
        print(f"{Fore.RED}{prefix} {message}{Style.RESET_ALL}")

    def verbose_msg(self, message: str, prefix: str = "~") -> None:
        """Print a verbose message (only when ``verbose`` is enabled)."""
        if self.verbose:
            print(f"{Fore.LIGHTBLACK_EX}{prefix} {message}{Style.RESET_ALL}")

    def action(self, message: str, prefix: str = "+") -> None:
        """Print an action message (blue)."""
        print(f"{Fore.BLUE}{prefix} {message}{Style.RESET_ALL}")

    def init(self, message: str, prefix: str = "🚀") -> None:
        """Print an initialization message (magenta)."""
        print(f"{Fore.MAGENTA}{prefix} {message}{Style.RESET_ALL}")

    def section(self, title: str, prefix: str = "=") -> None:
        """Print a section header with separator."""
        separator = prefix * (len(title) + 4)
        print(f"{Fore.CYAN}{separator}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{prefix} {title} {prefix}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{separator}{Style.RESET_ALL}")

    def config_display(self, config_data: dict, _title: str = "Configuration") -> None:
        """Display configuration data in a formatted ASCII box."""
        self.action("[EzQt_App] Loaded application settings.")
        if self.verbose:
            print(f"{Fore.LIGHTBLACK_EX}...{Style.RESET_ALL}")
            print(
                f"{Fore.LIGHTBLACK_EX}   ┌───────────────────────────────────────────────┐{Style.RESET_ALL}"
            )
            for key, val in config_data.items():
                print(
                    f"{Fore.LIGHTBLACK_EX}   |- {key}: {Fore.LIGHTWHITE_EX}{val}{Style.RESET_ALL}"
                )
            print(
                f"{Fore.LIGHTBLACK_EX}   └───────────────────────────────────────────────┘{Style.RESET_ALL}"
            )
            print(f"{Fore.LIGHTBLACK_EX}...{Style.RESET_ALL}")

    def list_items(
        self, items: list[str], title: str | None = None, max_items: int = 3
    ) -> None:
        """Print a (possibly truncated) list of items."""
        if title:
            self.info(title)
        if items:
            display_items = items[:max_items]
            items_str = ", ".join(display_items)
            if len(items) > max_items:
                items_str += "..."
            self.verbose_msg(f"   {items_str}")
        else:
            self.verbose_msg("   (no items)")

    def file_operation(
        self, operation: str, file_path: str, status: str = "completed"
    ) -> None:
        """Print a file operation message."""
        if status == "completed":
            self.info(f"[{operation}] {file_path}")
        elif status == "error":
            self.error(f"[{operation}] {file_path}")
        elif status == "warning":
            self.warning(f"[{operation}] {file_path}")

    def custom_print(
        self, message: str, color: str = "WHITE", prefix: str = ""
    ) -> None:
        """Print a message with an arbitrary colorama color name."""
        color_attr = getattr(Fore, color.upper(), Fore.WHITE)
        prefix_part = f"{prefix} " if prefix else ""
        print(f"{color_attr}{prefix_part}{message}{Style.RESET_ALL}")

    def raw_print(self, message: str) -> None:
        """Print a raw message without any formatting."""
        print(message)

    def qrc_compilation_result(
        self, success: bool, error_message: str | None = None
    ) -> None:
        """Print QRC compilation result."""
        if success:
            self.info("[FileMaker] Generated binaries definitions from QRC file.")
        else:
            self.warning("[FileMaker] QRC compilation skipped")
            if error_message:
                self.verbose_msg(f"Error details: {error_message}")


# ///////////////////////////////////////////////////////////////
# SINGLETONS
# ///////////////////////////////////////////////////////////////
_default_printer = Printer()


# ///////////////////////////////////////////////////////////////
# FUNCTIONS
# ///////////////////////////////////////////////////////////////
def get_printer(verbose: bool = False) -> Printer:
    """Return the global ``Printer`` instance, creating a new one if verbosity differs."""
    if verbose != _default_printer.verbose:
        return Printer(verbose)
    return _default_printer


def set_global_verbose(verbose: bool) -> None:
    """Set the global verbose mode on the default printer instance."""
    global _default_printer
    _default_printer = Printer(verbose)
