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
import subprocess  # nosec B404
from pathlib import Path

# Local imports
from ...domain.errors import (
    InvalidOverwritePolicyError,
    MissingPackageResourceError,
    ResourceCompilationError,
)
from ...utils.printer import get_printer
from ...utils.runtime_paths import APP_PATH

# Root of the installed ezqt_app package — used to locate bundled resources.
# Resolves correctly whether the package is installed (site-packages) or run
# in-place from the src/ layout.
_PKG_ROOT: Path = Path(__file__).parent.parent.parent


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

    _ERROR_CODES: dict[str, str] = {
        "invalid_overwrite_policy": "resources.invalid_overwrite_policy",
        "missing_yaml": "resources.missing_yaml",
        "missing_theme": "resources.missing_theme",
        "missing_translations": "resources.missing_translations",
        "qrc_compilation_failed": "resources.qrc_compilation_failed",
    }

    def __init__(
        self,
        base_path: Path | None = None,
        bin_path: Path | None = None,
        verbose: bool = False,
        overwrite_policy: str = "ask",
    ) -> None:
        self.base_path: Path = base_path or APP_PATH
        self._bin: Path = bin_path or (self.base_path / "bin")
        self._qrc_file: str = ""
        self._resources_module_file: str = ""
        self._overwrite_policy = overwrite_policy.lower().strip()
        if self._overwrite_policy not in {"ask", "skip", "force"}:
            raise InvalidOverwritePolicyError(
                code=self._error_code("invalid_overwrite_policy"),
                message=f"Unsupported overwrite policy: {overwrite_policy}",
                context={"supported": ["ask", "skip", "force"]},
            )
        self.printer = get_printer(verbose)

    # -----------------------------------------------------------
    # Error Code
    # -----------------------------------------------------------

    def _error_code(self, key: str) -> str:
        """Return a codified resource error code for a known key."""
        code = self._ERROR_CODES.get(key)
        if code is not None:
            return code
        slug = key.strip().lower().replace(" ", "_")
        return f"resources.{slug}"

    # -----------------------------------------------------------
    # Overwrite handling
    # -----------------------------------------------------------

    def _should_write(self, target_path: Path) -> bool:
        """Return whether a target file should be written according to policy."""
        if not target_path.exists():
            return True

        if self._overwrite_policy == "force":
            return True

        if self._overwrite_policy == "skip":
            self.printer.verbose_msg(f"Skipping existing file: {target_path}")
            return False

        # Default "ask": prompt interactively, otherwise skip for safety.
        try:
            import click

            if click.get_current_context(silent=True) is not None:
                return bool(click.confirm(f"Overwrite {target_path}?", default=False))
        except Exception as e:
            self.printer.verbose_msg(
                f"Could not prompt for overwrite decision ({target_path}): {e}"
            )

        self.printer.verbose_msg(f"Skipping existing file (ask policy): {target_path}")
        return False

    # -----------------------------------------------------------
    # High-level orchestrators
    # -----------------------------------------------------------

    def setup_project(
        self,
        mk_theme: bool = True,
        mk_config: bool = True,
        mk_translations: bool = True,
        build_resources: bool = True,
    ) -> bool:
        """Create directories and generate all assets."""
        try:
            self.make_assets_binaries()
            self.generate_all_assets(
                mk_theme=mk_theme,
                mk_config=mk_config,
                mk_translations=mk_translations,
                build_resources=build_resources,
            )
            return True
        except Exception as e:
            self.printer.error(f"Error setting up project: {e}")
            return False

    def generate_all_assets(
        self,
        mk_theme: bool = True,
        mk_config: bool = True,
        mk_translations: bool = True,
        build_resources: bool = True,
    ) -> bool:
        """Generate all required assets (YAML, QSS, translations, QRC, RC)."""
        try:
            self.make_assets_binaries()
            if mk_config:
                self.make_yaml_from_package()
            if mk_theme:
                self.make_qss_from_package()
            if mk_translations:
                self.make_translations_from_package()
            if build_resources and self.make_qrc():
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
        ]

        created_paths = []
        for path in paths_to_make:
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                created_paths.append(path)

        if created_paths:
            self.printer.action(
                f"[Initializer] Generated assets directories: {len(created_paths)} directories"
            )
            if verbose:
                self.printer.list_items([d.name for d in created_paths])

    def make_yaml_from_package(self, yaml_package: Path | None = None) -> Path | None:
        """Copy the package ``app.config.yaml`` into ``bin/config/``."""
        if yaml_package is None:
            yaml_package = _PKG_ROOT / "resources" / "config" / "app.config.yaml"

        if not yaml_package.exists():
            raise MissingPackageResourceError(
                code=self._error_code("missing_yaml"),
                message=f"YAML file not found at {yaml_package}",
                context={"resource": str(yaml_package)},
            )

        target_path = self._bin / "config" / "app.config.yaml"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._should_write(target_path):
            return target_path
        shutil.copy2(yaml_package, target_path)
        self.printer.action("[Initializer] Generated YAML config file.")
        return target_path

    def make_qss_from_package(self, theme_package: Path | None = None) -> bool:
        """Copy QSS theme files from the package into ``bin/themes/``."""
        if theme_package is None:
            theme_package = _PKG_ROOT / "resources" / "themes"

        if not theme_package.exists():
            raise MissingPackageResourceError(
                code=self._error_code("missing_theme"),
                message=f"Theme resource not found at {theme_package}",
                context={"resource": str(theme_package)},
            )

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
                    target_file = target_path / theme_package.name
                    if not self._should_write(target_file):
                        return True
                    shutil.copy2(theme_package, target_file)
                    self.printer.action("[Initializer] Generated QSS theme files.")
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
                        target_file = target_path / theme_file.name
                        if not self._should_write(target_file):
                            continue
                        shutil.copy2(theme_file, target_file)
                        copied_files.append(theme_file.name)
                        self.printer.verbose_msg(
                            f"Copied theme file: {theme_file.name}"
                        )
                    except Exception as e:
                        self.printer.warning(
                            f"Failed to copy theme file {theme_file.name}: {e}"
                        )

                if copied_files:
                    self.printer.action("[Initializer] Generated QSS theme files.")
                    return True

                existing = list(target_path.glob("*.qss"))
                if existing:
                    self.printer.info("[Initializer] QSS theme files already exist.")
                    return True

                self.printer.warning(
                    "[Initializer] No QSS theme files were copied successfully."
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
            translations_package = _PKG_ROOT / "resources" / "translations"

        if not translations_package.exists():
            raise MissingPackageResourceError(
                code=self._error_code("missing_translations"),
                message=f"Translations resource not found at {translations_package}",
                context={"resource": str(translations_package)},
            )

        target_path = self._bin / "translations"

        try:
            target_path.mkdir(parents=True, exist_ok=True)

            for translation_file in translations_package.glob("*.ts"):
                try:
                    target_file = target_path / translation_file.name
                    if not self._should_write(target_file):
                        continue
                    shutil.copy2(translation_file, target_file)
                    self.printer.verbose_msg(
                        f"Copied translation file: {translation_file.name}"
                    )
                except Exception as e:
                    self.printer.warning(
                        f"Failed to copy translation file {translation_file.name}: {e}"
                    )

            if any(target_path.glob("*.ts")):
                self.printer.action("[Initializer] Generated translation files.")
                return True

            self.printer.warning(
                "[Initializer] No translation files were copied successfully."
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

        def _add_qresource(directory: Path) -> None:
            if directory.exists():
                for file_path in directory.rglob("*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(self._bin).as_posix()
                        qrc_content.append(f"        <file>{relative_path}</file>")

        _add_qresource(self._bin / "fonts")
        _add_qresource(self._bin / "images")
        _add_qresource(self._bin / "icons")
        _add_qresource(self._bin / "themes")

        qrc_content.extend(["    </qresource>", "</RCC>"])

        qrc_file_path = self._bin / "resources.qrc"
        # resources.qrc is a derived build artifact: always refresh it.
        with open(qrc_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(qrc_content))

        self._qrc_file = str(qrc_file_path)
        self.printer.action("[Initializer] Generated QRC file from bin folder content.")
        return True

    def make_rc_py(self) -> None:
        """Compile the QRC file to a Python resource module via ``pyside6-rcc``."""
        if not self._qrc_file:
            self.printer.warning("[Initializer] No QRC file")
            return

        # resources_rc.py is a derived build artifact: always regenerate it.
        try:
            subprocess.run(  # nosec B603 B607
                ["pyside6-rcc", self._qrc_file, "-o", "resources_rc.py"],  # noqa: S607
                cwd=self._bin,
                check=True,
                capture_output=True,
            )
            self.printer.qrc_compilation_result(True)
        except subprocess.CalledProcessError as e:
            stderr_text = (
                e.stderr.decode("utf-8", errors="replace")
                if isinstance(e.stderr, bytes | bytearray)
                else str(e.stderr or "")
            )
            stdout_text = (
                e.stdout.decode("utf-8", errors="replace")
                if isinstance(e.stdout, bytes | bytearray)
                else str(e.stdout or "")
            )
            raise ResourceCompilationError(
                code=self._error_code("qrc_compilation_failed"),
                message="QRC compilation failed",
                context={
                    "details": str(e),
                    "qrc_file": self._qrc_file,
                    "stderr": stderr_text,
                    "stdout": stdout_text,
                },
            ) from e
        except FileNotFoundError as e:
            raise ResourceCompilationError(
                code=self._error_code("qrc_compilation_failed"),
                message="pyside6-rcc not found in PATH — install PySide6 or add it to your PATH",
                context={"tool": "pyside6-rcc", "qrc_file": self._qrc_file},
            ) from e

    def purge_rc_py(self) -> None:
        """Remove the generated ``resources_rc.py`` file."""
        rc_py_path = self._bin / "resources_rc.py"
        if rc_py_path.exists():
            rc_py_path.unlink()
            self.printer.warning("[Initializer] Purged resources_rc.py file.")

    def make_app_icons_py(self) -> None:
        """Generate typed accessor modules for user-compiled icon and image resources.

        Produces ``bin/app_icons.py`` (``AppIcons`` class) and
        ``bin/app_images.py`` (``AppImages`` class) from the files present in
        ``bin/icons/`` and ``bin/images/`` respectively.  Each file becomes a
        class attribute whose value is the corresponding Qt resource path
        (e.g. ``:/icons/my_icon.png``).
        """
        image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".ico", ".webp"}

        for dir_name, class_name, prefix, out_name in [
            ("icons", "AppIcons", ":/icons", "app_icons.py"),
            ("images", "AppImages", ":/images", "app_images.py"),
        ]:
            source_dir = self._bin / dir_name
            if not source_dir.exists():
                continue

            attrs: list[tuple[str, str]] = []
            for file_path in sorted(source_dir.rglob("*")):
                if file_path.is_file() and file_path.suffix.lower() in image_exts:
                    rel = file_path.relative_to(source_dir).as_posix()
                    parts = list(file_path.relative_to(source_dir).parts)
                    parts[-1] = Path(parts[-1]).stem
                    attr = "_".join(
                        p.replace("-", "_").replace(".", "_").replace(" ", "_")
                        for p in parts
                    )
                    attrs.append((attr, f"{prefix}/{rel}"))

            lines = [
                "# Auto-generated by ezqt_app — do not edit manually.",
                f"class {class_name}:",
                f'    """Typed accessor for compiled Qt resources under ``{prefix}/``."""',
                "",
            ]
            if attrs:
                for attr, qt_path in attrs:
                    lines.append(f'    {attr}: str = "{qt_path}"')
            else:
                lines.append("    pass")
            lines.append("")

            out_file = self._bin / out_name
            with open(out_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            if attrs:
                self.printer.action(
                    f"[Initializer] Generated {out_name} ({len(attrs)} entries)."
                )
            else:
                self.printer.verbose_msg(f"[Initializer] Generated {out_name} (empty).")

    def make_main_from_template(self, main_template: Path | None = None) -> None:
        """Copy the ``main.py`` project template into ``base_path``."""
        if main_template is None:
            main_template = _PKG_ROOT / "resources" / "templates" / "main.py.template"

        if not main_template.exists():
            self.printer.warning(f"Main template not found at {main_template}")
            return

        main_file = self.base_path / "main.py"
        if not self._should_write(main_file):
            return

        shutil.copy2(main_template, main_file)
        self.printer.action("[Initializer] Generated main.py file.")

    # -----------------------------------------------------------
    # Accessors
    # -----------------------------------------------------------

    def get_bin_path(self) -> Path:
        """Return the ``bin/`` directory path."""
        return self._bin

    def get_qrc_file(self) -> str:
        """Return the generated QRC file path."""
        return self._qrc_file

    def get_resources_module_file(self) -> str:
        """Return the generated resources module file path."""
        return self._resources_module_file
