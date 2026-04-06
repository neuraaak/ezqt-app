# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_THEME_SERVICE - ThemeService unit tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for ThemeService variable resolution."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from pathlib import Path
from typing import cast

# Local imports
from ezqt_app.domain.ports.main_window import MainWindowProtocol
from ezqt_app.services.ui.theme_service import ThemeService


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class TestThemeServiceResolveVariables:
    """Tests for ThemeService._resolve_variables."""

    def test_should_replace_single_var_reference_when_key_exists(self) -> None:
        """A single var(--name) token is substituted with its palette value."""
        stylesheet = "color: var(--base_text_color);"
        colors = {"base_text_color": "rgb(221, 221, 221)"}

        result = ThemeService._resolve_variables(stylesheet, colors)

        assert result == "color: rgb(221, 221, 221);"

    def test_should_replace_multiple_distinct_var_references(self) -> None:
        """Multiple distinct var(--x) tokens in the same stylesheet are all replaced."""
        stylesheet = (
            "background-color: var(--main_surface);\n"
            "border: 1px solid var(--main_border);"
        )
        colors = {
            "main_surface": "rgb(33, 37, 43)",
            "main_border": "rgb(44, 49, 58)",
        }

        result = ThemeService._resolve_variables(stylesheet, colors)

        assert "rgb(33, 37, 43)" in result
        assert "rgb(44, 49, 58)" in result
        assert "var(--" not in result

    def test_should_replace_repeated_var_reference_all_occurrences(self) -> None:
        """A var token repeated multiple times is replaced at every occurrence."""
        stylesheet = "background: var(--main_surface);\ncolor: var(--main_surface);"
        colors = {"main_surface": "rgb(33, 37, 43)"}

        result = ThemeService._resolve_variables(stylesheet, colors)

        assert result.count("rgb(33, 37, 43)") == 2
        assert "var(--" not in result

    def test_should_preserve_unresolved_token_when_key_missing(self) -> None:
        """A var(--x) token whose key is absent from the palette is left unchanged."""
        stylesheet = "color: var(--unknown_var);"
        colors = {"main_surface": "rgb(33, 37, 43)"}

        result = ThemeService._resolve_variables(stylesheet, colors)

        assert "var(--unknown_var)" in result

    def test_should_return_stylesheet_unchanged_when_colors_empty(self) -> None:
        """An empty color mapping leaves all var(--x) tokens in place."""
        stylesheet = "color: var(--base_text_color);"

        result = ThemeService._resolve_variables(stylesheet, {})

        assert result == stylesheet

    def test_should_return_stylesheet_unchanged_when_no_var_tokens(self) -> None:
        """A stylesheet without var(--x) tokens is returned verbatim."""
        stylesheet = "QWidget { color: rgb(255, 255, 255); }"
        colors = {"main_surface": "rgb(33, 37, 43)"}

        result = ThemeService._resolve_variables(stylesheet, colors)

        assert result == stylesheet

    def test_should_handle_hex_color_values(self) -> None:
        """Hex color values are inserted correctly."""
        stylesheet = "background-color: var(--main_accent_color);"
        colors = {"main_accent_color": "#96CD32"}

        result = ThemeService._resolve_variables(stylesheet, colors)

        assert result == "background-color: #96CD32;"

    def test_should_handle_rgba_color_values(self) -> None:
        """RGBA color values with commas and spaces are inserted without modification."""
        stylesheet = "background: var(--semi_transparent);"
        colors = {"semi_transparent": "rgba(33, 37, 43, 180)"}

        result = ThemeService._resolve_variables(stylesheet, colors)

        assert result == "background: rgba(33, 37, 43, 180);"

    def test_should_not_match_malformed_var_syntax(self) -> None:
        """Tokens that do not match var(--name) exactly are left unchanged."""
        stylesheet = 'color: --var("main_surface"); font: var("main_surface");'
        colors = {"main_surface": "rgb(33, 37, 43)"}

        result = ThemeService._resolve_variables(stylesheet, colors)

        assert '--var("main_surface")' in result
        assert 'var("main_surface")' in result


class TestThemeServiceGetAvailableThemes:
    """Tests for ThemeService.get_available_themes."""

    def test_should_return_list_of_tuples_when_palette_has_presets(
        self, monkeypatch
    ) -> None:
        """Each preset × variant pair produces a (display, internal) tuple."""
        import ezqt_app.services.ui.theme_service as ts_module

        fake_config = {
            "palette": {
                "blue-gray": {"dark": {}, "light": {}},
                "github-dark": {"dark": {}},
            }
        }

        class _FakeConfigService:
            def load_config(self, _name: str):
                return fake_config

        monkeypatch.setattr(
            ts_module, "get_config_service", lambda: _FakeConfigService()
        )

        options = ThemeService.get_available_themes()

        assert len(options) == 3
        labels = [label for label, _ in options]
        values = [val for _, val in options]
        assert "Blue Gray - Dark" in labels
        assert "Blue Gray - Light" in labels
        assert "Github Dark - Dark" in labels
        assert "blue-gray:dark" in values
        assert "blue-gray:light" in values
        assert "github-dark:dark" in values

    def test_should_return_empty_list_when_palette_is_missing(
        self, monkeypatch
    ) -> None:
        """No presets → empty options list."""
        import ezqt_app.services.ui.theme_service as ts_module

        class _FakeConfigService:
            def load_config(self, _name: str):
                return {}

        monkeypatch.setattr(
            ts_module, "get_config_service", lambda: _FakeConfigService()
        )

        options = ThemeService.get_available_themes()

        assert options == []


class TestThemeServiceApplyAndLoad:
    """Tests for ThemeService.apply_theme and theme file loading branches."""

    def test_should_apply_resolved_stylesheet_on_window(self, monkeypatch) -> None:
        import ezqt_app.services.ui.theme_service as ts_module

        class _FakeSettings:
            class gui:  # noqa: N801
                THEME_PRESET = "blue-gray"
                THEME = "dark"

        class _FakeConfigService:
            def load_config(self, _name: str):
                return {
                    "palette": {"blue-gray": {"dark": {"main_surface": "rgb(1, 2, 3)"}}}
                }

        class _FakeStyleSheet:
            def __init__(self) -> None:
                self.value = ""

            def setStyleSheet(self, value: str) -> None:  # noqa: N802
                self.value = value

        class _FakeUi:
            def __init__(self) -> None:
                self.style_sheet = _FakeStyleSheet()

        class _FakeWindow:
            def __init__(self) -> None:
                self.ui = _FakeUi()

        monkeypatch.setattr(ts_module, "get_settings_service", lambda: _FakeSettings())
        monkeypatch.setattr(
            ts_module, "get_config_service", lambda: _FakeConfigService()
        )
        monkeypatch.setattr(
            ts_module,
            "_load_themes_content",
            lambda: "QWidget { background: var(--main_surface); }",
            raising=False,
        )
        monkeypatch.setattr(
            ts_module.ThemeService,
            "_load_themes_content",
            staticmethod(lambda: "QWidget { background: var(--main_surface); }"),
        )

        window = _FakeWindow()
        ThemeService.apply_theme(cast(MainWindowProtocol, window))

        assert "rgb(1, 2, 3)" in window.ui.style_sheet.value
        assert window.ui.style_sheet.value.endswith("\n")

    def test_should_load_local_themes_and_skip_qtstrap(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        import ezqt_app.services.ui.theme_service as ts_module

        local_themes = tmp_path / "bin" / "themes"
        local_themes.mkdir(parents=True)
        (local_themes / "b.qss").write_text("B", encoding="utf-8")
        (local_themes / "a.qss").write_text("A", encoding="utf-8")
        (local_themes / "qtstrap.qss").write_text("SKIP", encoding="utf-8")

        monkeypatch.setattr(ts_module, "get_bin_path", lambda: tmp_path / "bin")

        merged = ThemeService._load_themes_content()

        assert merged == "A\n\nB"

    def test_should_fallback_to_package_themes_when_local_is_empty(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        import ezqt_app.services.ui.theme_service as ts_module

        fake_module_file = (
            tmp_path / "pkg" / "ezqt_app" / "services" / "ui" / "theme_service.py"
        )
        fake_module_file.parent.mkdir(parents=True, exist_ok=True)
        fake_module_file.write_text("# fake", encoding="utf-8")

        package_themes = tmp_path / "pkg" / "ezqt_app" / "resources" / "themes"
        package_themes.mkdir(parents=True)
        (package_themes / "theme.qss").write_text("PKG", encoding="utf-8")

        monkeypatch.setattr(ts_module, "get_bin_path", lambda: tmp_path / "missing_bin")
        monkeypatch.setattr(ts_module, "__file__", str(fake_module_file))

        merged = ThemeService._load_themes_content()

        assert merged == "PKG"

    def test_should_raise_file_not_found_when_no_qss_files_exist(
        self, tmp_path: Path, monkeypatch
    ) -> None:
        import ezqt_app.services.ui.theme_service as ts_module

        fake_module_file = (
            tmp_path / "pkg" / "ezqt_app" / "services" / "ui" / "theme_service.py"
        )
        fake_module_file.parent.mkdir(parents=True, exist_ok=True)
        fake_module_file.write_text("# fake", encoding="utf-8")

        monkeypatch.setattr(ts_module, "get_bin_path", lambda: tmp_path / "missing_bin")
        monkeypatch.setattr(ts_module, "__file__", str(fake_module_file))

        import pytest

        with pytest.raises(FileNotFoundError):
            ThemeService._load_themes_content()
