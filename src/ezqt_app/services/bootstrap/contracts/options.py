# ///////////////////////////////////////////////////////////////
# SERVICES.BOOTSTRAP.CONTRACTS.OPTIONS - Init options and policies
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Contracts for initialization options and overwrite behavior."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


# ///////////////////////////////////////////////////////////////
# TYPES
# ///////////////////////////////////////////////////////////////
class OverwritePolicy(StrEnum):
    """Policy used when generated files already exist."""

    ASK = "ask"
    SKIP = "skip"
    FORCE = "force"


# ///////////////////////////////////////////////////////////////
# MODELS
# ///////////////////////////////////////////////////////////////
@dataclass(slots=True)
class InitOptions:
    """Options driving initialization behavior across API and CLI.

    Attributes:
        project_root: Absolute path to the project root directory. When
            ``None``, defaults to ``Path.cwd()`` at resolve time.
        bin_path: Directory where generated assets (``resources_rc.py``,
            ``app_icons.py``, ``app_images.py``, themes) are written.
            When ``None``, defaults to ``<project_root>/bin``. A relative
            value is resolved against ``project_root``; an absolute value is
            used as-is.
        mk_theme: Generate QSS theme files under ``bin_path/themes/``.
        mk_config: Generate the ``config/`` YAML files.
        mk_translations: Generate the ``translations/`` TS source files.
        build_resources: Compile the QRC file with ``pyside6-rcc`` and write
            ``resources_rc.py``, ``app_icons.py``, and ``app_images.py``
            into ``bin_path``. Raises ``ResourceCompilationError`` if
            ``pyside6-rcc`` is not found on ``PATH``.
        generate_main: Write a ``main.py`` entrypoint in the project root.
        verbose: Print step-by-step progress to stdout.
        overwrite_policy: Controls behavior when generated files already
            exist. See :class:`OverwritePolicy`.
    """

    project_root: Path | None = None
    bin_path: Path | None = None
    mk_theme: bool = True
    mk_config: bool = True
    mk_translations: bool = True
    build_resources: bool = True
    generate_main: bool = False
    verbose: bool = True
    overwrite_policy: OverwritePolicy = OverwritePolicy.ASK

    def resolve(self) -> InitOptions:
        """Return a copy with normalized paths and defaults resolved."""
        root = self.project_root or Path.cwd()
        if self.bin_path is None:
            bin_path = root / "bin"
        elif not self.bin_path.is_absolute():
            bin_path = (root / self.bin_path).resolve()
        else:
            bin_path = self.bin_path

        return InitOptions(
            project_root=root,
            bin_path=bin_path,
            mk_theme=self.mk_theme,
            mk_config=self.mk_config,
            mk_translations=self.mk_translations,
            build_resources=self.build_resources,
            generate_main=self.generate_main,
            verbose=self.verbose,
            overwrite_policy=self.overwrite_policy,
        )
