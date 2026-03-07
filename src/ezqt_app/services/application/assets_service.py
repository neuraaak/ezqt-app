# ///////////////////////////////////////////////////////////////
# SERVICES.APPLICATION.ASSETS_SERVICE - Assets orchestration service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Orchestrates asset generation and requirements checks for EzQt_App projects."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
from pathlib import Path

# Local imports
from ..config.config_service import get_package_resource
from .file_service import FileService


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class AssetsService:
    """Orchestrates asset generation and requirement checks.

    Delegates file-level operations to :class:`FileService` and exposes
    higher-level workflows used during application initialisation.
    """

    @staticmethod
    def check_assets_requirements() -> None:
        """Generate asset binaries, QRC and RC files at APP_PATH."""
        maker = FileService()  # defaults to APP_PATH
        maker.make_assets_binaries()
        res = maker.make_qrc()
        maker.make_rc_py() if res else maker.purge_rc_py()
        maker.make_app_resources_module()

    @staticmethod
    def make_app_resources_module() -> None:
        """Generate (no-op in v5) the application resources module."""
        FileService().make_app_resources_module()

    @staticmethod
    def make_required_files(mk_theme: bool = True) -> None:
        """Copy YAML, QSS theme and translation files into ``cwd/bin/``.

        Parameters
        ----------
        mk_theme:
            When ``True`` (default) also copies the QSS theme file.
        """
        yaml_package = get_package_resource("app.yaml")
        FileService(Path.cwd()).make_yaml_from_package(yaml_package)

        if mk_theme:
            theme_package = get_package_resource("resources/themes/main_theme.qss")
            FileService(Path.cwd()).make_qss_from_package(theme_package)

        translations_package = get_package_resource("resources/translations")
        FileService(Path.cwd()).make_translations_from_package(translations_package)
