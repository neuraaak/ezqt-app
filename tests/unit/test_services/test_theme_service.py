# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_SERVICES.TEST_THEME_SERVICE - ThemeService unit tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for ThemeService variable resolution."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Local imports
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
