# ///////////////////////////////////////////////////////////////
# SHARED.RESOURCES - Shared resource definitions
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Shared static resource path definitions."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import TypeVar, cast

# Local imports
from ...resources import base_resources_rc  # noqa: F401
from ...utils.runtime_paths import APP_PATH
from .icons import Icons as _PackageIcons
from .images import Images as _PackageImages

# Expose packaged defaults early so optional runtime modules importing
# ezqt_app.shared.resources can resolve these names during bootstrap.
Icons = _PackageIcons
Images = _PackageImages

T = TypeVar("T")


def _load_module_from_file(module_name: str, file_path: Path) -> ModuleType | None:
    """Import a Python module directly from file when it exists."""
    if not file_path.exists() or not file_path.is_file():
        return None

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None

    sys.modules[module_name] = module
    return module


def _select_resource_class(
    module: ModuleType | None,
    class_names: tuple[str, ...],
    fallback: type[T],
) -> type[T]:
    """Return the first matching class from a module, otherwise fallback."""
    if module is None:
        return fallback

    for class_name in class_names:
        candidate = getattr(module, class_name, None)
        if isinstance(candidate, type):
            return cast(type[T], candidate)
    return fallback


def _load_runtime_resources() -> tuple[type[_PackageIcons], type[_PackageImages]]:
    """Load runtime-generated resources from project folders when available."""
    # Register user-generated Qt resources without replacing packaged fallback.
    _load_module_from_file(
        "ezqt_app._runtime_resources_rc", APP_PATH / "bin" / "resources_rc.py"
    )

    runtime_icons_module = _load_module_from_file(
        "ezqt_app._runtime_icons", APP_PATH / "modules" / "icons.py"
    )
    runtime_images_module = _load_module_from_file(
        "ezqt_app._runtime_images", APP_PATH / "modules" / "images.py"
    )
    runtime_app_module = _load_module_from_file(
        "ezqt_app._runtime_app_resources", APP_PATH / "modules" / "app_resources.py"
    )

    icons_cls = _select_resource_class(
        runtime_icons_module,
        ("AppIcons", "Icons"),
        _select_resource_class(
            runtime_app_module, ("AppIcons", "Icons"), _PackageIcons
        ),
    )
    images_cls = _select_resource_class(
        runtime_images_module,
        ("AppImages", "Images"),
        _select_resource_class(
            runtime_app_module, ("AppImages", "Images"), _PackageImages
        ),
    )
    return icons_cls, images_cls


_runtime_icons, _runtime_images = _load_runtime_resources()
Icons: type[_PackageIcons] = _runtime_icons
Images: type[_PackageImages] = _runtime_images

# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["Icons", "Images"]
