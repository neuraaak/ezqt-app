# ///////////////////////////////////////////////////////////////
# EZPL - Shared CLI Console
# Project: ezpl
# ///////////////////////////////////////////////////////////////

"""
Shared Rich Console instance for all CLI modules.

Centralizes Console creation so that output configuration
(e.g., no_color, stderr, force_terminal) can be adjusted in one place.
"""

from __future__ import annotations

# Third-party imports
from rich.console import Console

# ///////////////////////////////////////////////////////////////
# SHARED INSTANCE
# ///////////////////////////////////////////////////////////////

console: Console = Console()
