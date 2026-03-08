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
from enum import Enum
from pathlib import Path


# ///////////////////////////////////////////////////////////////
# TYPES
# ///////////////////////////////////////////////////////////////
class OverwritePolicy(str, Enum):
    """Policy used when generated files already exist."""

    ASK = "ask"
    SKIP = "skip"
    FORCE = "force"


# ///////////////////////////////////////////////////////////////
# MODELS
# ///////////////////////////////////////////////////////////////
@dataclass(slots=True)
class InitOptions:
    """Options driving initialization behavior across API and CLI."""

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
        bin_path = self.bin_path or (root / "bin")

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
