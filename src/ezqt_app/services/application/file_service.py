# ///////////////////////////////////////////////////////////////
# SERVICES.APPLICATION.FILE_SERVICE - File generation service
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""File and resource generation service for EzQt_App projects."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import shutil
import subprocess
from pathlib import Path

# Local imports
from ...utils.printer import get_printer
from ...utils.runtime_paths import APP_PATH


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class FileService:
    """Handles file and resource generation for EzQt_App projects.

    Manages generation of:
    - Asset directories
    - Configuration files (YAML)
    - Theme files (QSS)
    - Translation files (.ts)
    - Resource files (.qrc, _rc.py)
    - Project templates
    """

    def __init__(self, base_path: Path | None = None, verbose: bool = False) -> None:
        self.base_path: Path = base_path or APP_PATH
        self._bin: Path = self.base_path / "bin"
        self._modules: Path = self.base_path / "modules"
        self._qrc_file: str = ""
        self._resources_module_file: str = ""
        self.printer = get_printer(verbose)

    # -----------------------------------------------------------
    # High-level orchestrators
    # -----------------------------------------------------------

    def setup_project(self) -> bool:
        """Create directories and generate all assets."""
        try:
            self.make_assets_binaries()
            self.generate_all_assets()
            return True
        except Exception as e:
            self.printer.error(f"Error setting up project: {e}")
            return False

    def generate_all_assets(self) -> bool:
        """Generate all required assets (YAML, QSS, translations, QRC, RC)."""
        try:
            self.make_assets_binaries()
            self.make_yaml_from_package()
            self.make_qss_from_package()
            self.make_translations_from_package()
            self.make_qrc()
            self.make_rc_py()
            return True
        except Exception as e:
            self.printer.error(f"Error generating assets: {e}")
            return False

    # -----------------------------------------------------------
    # Directory / file creation
    # -----------------------------------------------------------

    def make_assets_binaries(self, verbose: bool = False) -> None:
        """Create the standard binary directory tree under ``bin/``."""
        paths_to_make: list[Path] = [
            self._bin,
            self._bin / "fonts",
            self._bin / "images",
            self._bin / "icons",
            self._bin / "themes",
            self._bin / "config",
            self._bin / "translations",
            self._modules,
        ]

        created_paths = []
        for path in paths_to_make:
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                created_paths.append(path)

        if created_paths:
            self.printer.info(
                f"[FileMaker] Generated assets directories: {len(created_paths)} directories"
            )
            if verbose:
                self.printer.list_items([d.name for d in created_paths])

    def make_yaml_from_package(self, yaml_package: Path | None = None) -> Path | None:
        """Copy the package ``app.yaml`` into ``bin/config/``."""
        if yaml_package is None:
            import pkg_resources  # type: ignore[import-untyped]

            yaml_package = Path(pkg_resources.resource_filename("ezqt_app", "app.yaml"))

        if not yaml_package.exists():
            self.printer.warning(f"YAML file not found at {yaml_package}")
            return None

        target_path = self._bin / "config" / "app.yaml"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(yaml_package, target_path)
        self.printer.info("[FileMaker] Generated YAML config file.")
        return target_path

    def make_qss_from_package(self, theme_package: Path | None = None) -> bool:
        """Copy QSS theme files from the package into ``bin/themes/``."""
        if theme_package is None:
            import pkg_resources  # type: ignore[import-untyped]

            theme_package = Path(
                pkg_resources.resource_filename("ezqt_app", "resources/themes")
            )

        if not theme_package.exists():
            self.printer.warning(f"Theme directory not found at {theme_package}")
            return False

        target_path = self._bin / "themes"

        try:
            target_path.mkdir(parents=True, exist_ok=True)

            if theme_package.is_file():
                if theme_package.name == "qtstrap.qss":
                    self.printer.verbose_msg(
                        f"Skipping unnecessary theme file: {theme_package.name}"
                    )
                    return False
                try:
                    shutil.copy2(theme_package, target_path / theme_package.name)
                    self.printer.info("[FileMaker] Generated QSS theme files.")
                    return True
                except Exception as e:
                    self.printer.warning(
                        f"Failed to copy theme file {theme_package.name}: {e}"
                    )
                    return False
            else:
                copied_files = []
                for theme_file in theme_package.glob("*.qss"):
                    if theme_file.name == "qtstrap.qss":
                        self.printer.verbose_msg(
                            f"Skipping unnecessary theme file: {theme_file.name}"
                        )
                        continue
                    try:
                        shutil.copy2(theme_file, target_path / theme_file.name)
                        copied_files.append(theme_file.name)
                        self.printer.verbose_msg(
                            f"Copied theme file: {theme_file.name}"
                        )
                    except Exception as e:
                        self.printer.warning(
                            f"Failed to copy theme file {theme_file.name}: {e}"
                        )

                if copied_files:
                    self.printer.info("[FileMaker] Generated QSS theme files.")
                    return True

                existing = list(target_path.glob("*.qss"))
                if existing:
                    self.printer.info("[FileMaker] QSS theme files already exist.")
                    return True

                self.printer.warning(
                    "[FileMaker] No QSS theme files were copied successfully."
                )
                return False

        except Exception as e:
            self.printer.error(f"Error copying theme files: {e}")
            return False

    def make_translations_from_package(
        self, translations_package: Path | None = None
    ) -> bool:
        """Copy ``.ts`` translation files from the package into ``bin/translations/``."""
        if translations_package is None:
            import pkg_resources  # type: ignore[import-untyped]

            translations_package = Path(
                pkg_resources.resource_filename("ezqt_app", "resources/translations")
            )

        if not translations_package.exists():
            self.printer.warning(
                f"Translations directory not found at {translations_package}"
            )
            return False

        target_path = self._bin / "translations"

        try:
            target_path.mkdir(parents=True, exist_ok=True)

            for translation_file in translations_package.glob("*.ts"):
                try:
                    shutil.copy2(translation_file, target_path / translation_file.name)
                    self.printer.verbose_msg(
                        f"Copied translation file: {translation_file.name}"
                    )
                except Exception as e:
                    self.printer.warning(
                        f"Failed to copy translation file {translation_file.name}: {e}"
                    )

            if any(target_path.glob("*.ts")):
                self.printer.info("[FileMaker] Generated translation files.")
                return True

            self.printer.warning(
                "[FileMaker] No translation files were copied successfully."
            )
            return False

        except Exception as e:
            self.printer.error(f"Error copying translation files: {e}")
            return False

    def make_qrc(self) -> bool:
        """Generate a ``resources.qrc`` file from the ``bin/`` directory contents."""
        qrc_content = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            "<RCC>",
            '    <qresource prefix="/">',
        ]

        def _add_qresource(directory: Path, prefix: str) -> None:
            if directory.exists():
                for file_path in directory.rglob("*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(self._bin)
                        qrc_content.append(
                            f"        <file>{prefix}/{relative_path}</file>"
                        )

        _add_qresource(self._bin / "fonts", "fonts")
        _add_qresource(self._bin / "images", "images")
        _add_qresource(self._bin / "icons", "icons")
        _add_qresource(self._bin / "themes", "themes")
        _add_qresource(self._bin / "config", "config")
        _add_qresource(self._bin / "translations", "translations")

        qrc_content.extend(["    </qresource>", "</RCC>"])

        qrc_file_path = self._bin / "resources.qrc"
        with open(qrc_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(qrc_content))

        self._qrc_file = str(qrc_file_path)
        self.printer.info("[FileMaker] Generated QRC file from bin folder content.")
        return True

    def make_rc_py(self) -> None:
        """Compile the QRC file to a Python resource module via ``pyside6-rcc``."""
        if not self._qrc_file:
            self.printer.warning("[FileMaker] No QRC file")
            return

        try:
            subprocess.run(
                ["pyside6-rcc", self._qrc_file, "-o", "resources_rc.py"],  # noqa: S607
                cwd=self._bin,
                check=True,
                capture_output=True,
            )
            self.printer.qrc_compilation_result(True)
        except subprocess.CalledProcessError as e:
            self.printer.qrc_compilation_result(False, str(e))
        except FileNotFoundError:
            self.printer.qrc_compilation_result(False, "pyside6-rcc not found")

    def purge_rc_py(self) -> None:
        """Remove the generated ``resources_rc.py`` file."""
        rc_py_path = self._bin / "resources_rc.py"
        if rc_py_path.exists():
            rc_py_path.unlink()
            self.printer.info("[FileMaker] Purged resources_rc.py file.")

    def make_app_resources_module(self) -> None:
        """Legacy no-op — v5 uses ``ezqt_app.shared.resources`` directly."""
        self._resources_module_file = ""
        self.printer.info(
            "[FileMaker] app_resources.py generation skipped (v5 uses ezqt_app.shared.resources)."
        )

    def make_main_from_template(self, main_template: Path | None = None) -> None:
        """Copy the ``main.py`` project template into ``base_path``."""
        if main_template is None:
            main_template = APP_PATH / "resources" / "templates" / "main.py.template"

        if not main_template.exists():
            self.printer.warning(f"Main template not found at {main_template}")
            return

        shutil.copy2(main_template, self.base_path / "main.py")
        self.printer.info("[FileMaker] Generated main.py file.")

    # -----------------------------------------------------------
    # Accessors
    # -----------------------------------------------------------

    def get_bin_path(self) -> Path:
        """Return the ``bin/`` directory path."""
        return self._bin

    def get_modules_path(self) -> Path:
        """Return the ``modules/`` directory path."""
        return self._modules

    def get_qrc_file(self) -> str:
        """Return the generated QRC file path."""
        return self._qrc_file

    def get_resources_module_file(self) -> str:
        """Return the generated resources module file path."""
        return self._resources_module_file
