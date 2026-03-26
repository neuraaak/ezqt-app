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
    def check_assets_requirements(
        base_path: Path | None = None,
        bin_path: Path | None = None,
        overwrite_policy: str = "ask",
    ) -> None:
        """Generate asset binaries, QRC and RC files at APP_PATH."""
        maker = FileService(
            base_path=base_path,
            bin_path=bin_path,
            overwrite_policy=overwrite_policy,
        )
        maker.make_assets_binaries()
        res = maker.make_qrc()
        if res:
            maker.make_rc_py()
            maker.make_app_icons_py()
        else:
            maker.purge_rc_py()

    @staticmethod
    def make_required_files(
        mk_theme: bool = True,
        mk_config: bool = True,
        mk_translations: bool = True,
        base_path: Path | None = None,
        bin_path: Path | None = None,
        overwrite_policy: str = "ask",
    ) -> None:
        """Copy YAML, QSS theme and translation files into ``cwd/bin/``.

        Parameters
        ----------
        mk_theme:
            When ``True`` (default) also copies the QSS theme file.
        """
        project_root = base_path or Path.cwd()
        maker = FileService(
            base_path=project_root,
            bin_path=bin_path,
            overwrite_policy=overwrite_policy,
        )

        if mk_config:
            yaml_package = get_package_resource("resources/config/app.config.yaml")
            maker.make_yaml_from_package(yaml_package)

        if mk_theme:
            theme_package = get_package_resource("resources/themes")
            maker.make_qss_from_package(theme_package)

        if mk_translations:
            translations_package = get_package_resource("resources/translations")
            maker.make_translations_from_package(translations_package)
