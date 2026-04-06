# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SHARED_RESOURCES - Shared resources tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for shared/resources/__init__.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
import sys
from pathlib import Path

from ezqt_app.shared import resources


class TestRuntimeResourceLoading:
    """Tests for runtime module loading helpers."""

    def test_should_return_none_when_runtime_module_file_is_missing(
        self, tmp_path: Path
    ) -> None:
        mod = resources._load_module_from_file(
            "ezqt_app._missing_runtime", tmp_path / "x.py"
        )
        assert mod is None

    def test_should_load_module_from_file_when_python_file_is_valid(
        self, tmp_path: Path
    ) -> None:
        runtime_file = tmp_path / "runtime_mod.py"
        runtime_file.write_text("VALUE = 7\n", encoding="utf-8")

        module_name = "ezqt_app._runtime_test_valid"
        mod = resources._load_module_from_file(module_name, runtime_file)

        assert mod is not None
        assert mod.VALUE == 7
        assert module_name in sys.modules

    def test_should_return_none_when_runtime_module_exec_fails(
        self, tmp_path: Path
    ) -> None:
        bad_file = tmp_path / "bad_mod.py"
        bad_file.write_text("raise RuntimeError('broken')\n", encoding="utf-8")

        mod = resources._load_module_from_file("ezqt_app._runtime_bad", bad_file)

        assert mod is None

    def test_should_load_runtime_icons_and_images_when_files_exist(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        (tmp_path / "resources_rc.py").write_text("# rc\n", encoding="utf-8")
        (tmp_path / "app_icons.py").write_text(
            "class AppIcons:\n    check: str = ':/icons/check.png'\n",
            encoding="utf-8",
        )
        (tmp_path / "app_images.py").write_text(
            "class AppImages:\n    hero: str = ':/images/hero.png'\n",
            encoding="utf-8",
        )

        monkeypatch.setattr(resources, "get_bin_path", lambda: tmp_path)

        resources.load_runtime_rc()

        assert resources.AppIcons is not None
        assert resources.AppImages is not None
        assert resources.AppIcons.check == ":/icons/check.png"
        assert resources.AppImages.hero == ":/images/hero.png"
