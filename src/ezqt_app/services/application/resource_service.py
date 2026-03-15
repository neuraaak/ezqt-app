# ///////////////////////////////////////////////////////////////
# SERVICES.APPLICATION.RESOURCE_SERVICE - Qt resource loader
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Qt resource loading service — fonts via QFontDatabase."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from PySide6.QtGui import QFontDatabase

from ...utils.printer import get_printer
from ...utils.runtime_paths import APP_PATH

# Local imports
from ..config.config_service import get_package_resource


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ResourceService:
    """Loads Qt resources (fonts) from the package and the application bin."""

    @staticmethod
    def load_fonts_resources(app: bool = False) -> None:
        """Load ``.ttf`` font files into Qt's font database.

        Parameters
        ----------
        app:
            When ``False`` loads from the installed package resources,
            then recurses with ``app=True`` to also load from ``bin/fonts/``.
            When ``True`` loads from the project ``bin/fonts/`` directory.
        """
        if not app:
            fonts = get_package_resource("resources/fonts")
            source = "Package"
        else:
            fonts = APP_PATH / "bin" / "fonts"
            source = "Application"

        if not fonts.exists():
            return

        printer = get_printer()
        for font in fonts.iterdir():
            if font.suffix == ".ttf":
                font_id = QFontDatabase.addApplicationFont(str(font))
                if font_id == -1:
                    printer.error(
                        f"[System] Failed to load font from {source}: {font.stem}."
                    )
                else:
                    printer.action(f"[System] Font loaded from {source}: {font.stem}.")

        # Recurse to also load application-level fonts
        if not app:
            ResourceService.load_fonts_resources(app=True)
