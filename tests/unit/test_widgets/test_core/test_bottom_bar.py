# ///////////////////////////////////////////////////////////////
# TESTS.UNIT.TEST_WIDGETS.TEST_CORE.TEST_BOTTOM_BAR - BottomBar tests
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Unit tests for widgets/core/bottom_bar.py."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
from PySide6.QtWidgets import QFrame, QLabel, QWidget

from ezqt_app.widgets.core.bottom_bar import BottomBar

# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////


class TestBottomBarInit:
    """Tests for BottomBar initialization and structure."""

    def test_should_create_widget_when_instantiated(self, qt_application) -> None:
        bar = BottomBar()
        assert bar is not None

    def test_should_have_bottom_bar_object_name_when_instantiated(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        assert bar.objectName() == "bottomBar"

    def test_should_have_no_frame_shape_when_instantiated(self, qt_application) -> None:
        bar = BottomBar()
        assert bar.frameShape() == QFrame.Shape.NoFrame

    def test_should_have_raised_frame_shadow_when_instantiated(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        assert bar.frameShadow() == QFrame.Shadow.Raised

    def test_should_have_horizontal_layout_when_instantiated(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        assert hasattr(bar, "HL_bottomBar")
        assert bar.HL_bottomBar is not None

    def test_should_have_credits_label_when_instantiated(self, qt_application) -> None:
        bar = BottomBar()
        assert hasattr(bar, "creditsLabel")
        assert isinstance(bar.creditsLabel, QLabel)

    def test_should_have_version_label_when_instantiated(self, qt_application) -> None:
        bar = BottomBar()
        assert hasattr(bar, "version")
        assert isinstance(bar.version, QLabel)

    def test_should_have_size_grip_frame_when_instantiated(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        assert hasattr(bar, "appSizeGrip")
        assert isinstance(bar.appSizeGrip, QFrame)

    def test_should_have_minimum_height_of_22_when_instantiated(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        assert bar.minimumHeight() == 22

    def test_should_have_maximum_height_of_22_when_instantiated(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        assert bar.maximumHeight() == 22

    def test_should_accept_parent_widget_when_instantiated_with_parent(
        self, qt_application
    ) -> None:
        parent = QWidget()
        bar = BottomBar(parent=parent)
        assert bar.parent() is parent


class TestBottomBarSetCredits:
    """Tests for BottomBar.set_credits()."""

    def test_should_not_raise_when_set_credits_is_called_with_plain_text(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.set_credits("Made by Test Author")
        # Must not raise

    def test_should_set_pointing_hand_cursor_when_set_credits_is_called_with_email(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.set_credits({"name": "Test Author", "email": "author@example.com"})
        # Cursor must be pointing hand because email is present
        from PySide6.QtCore import Qt

        assert bar.creditsLabel.cursor().shape() == Qt.CursorShape.PointingHandCursor

    def test_should_not_raise_when_set_credits_is_called_with_name_only(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.set_credits({"name": "Test Author"})
        # Must not raise — no email so no clickable link

    def test_should_use_default_when_set_credits_is_called_with_empty_dict(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.set_credits({})
        # Must not raise

    def test_should_use_default_when_set_credits_is_called_with_invalid_type(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        # 123 is invalid — the method catches exceptions internally
        bar.set_credits(123)  # type: ignore[arg-type]


class TestBottomBarSetVersion:
    """Tests for BottomBar.set_version_auto()."""

    def test_should_not_raise_when_set_version_auto_is_called(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.set_version_auto()

    def test_should_have_right_alignment_when_version_label_is_created(
        self, qt_application
    ) -> None:
        from PySide6.QtCore import Qt

        bar = BottomBar()
        alignment = bar.version.alignment()
        assert (
            Qt.AlignmentFlag.AlignRight in alignment
            or Qt.AlignmentFlag.AlignTrailing in alignment
        )


class TestBottomBarTranslationIndicator:
    """Tests for the translation-in-progress indicator widget."""

    def test_should_have_translation_indicator_label_when_instantiated(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        assert hasattr(bar, "translationIndicator")
        assert isinstance(bar.translationIndicator, QLabel)

    def test_should_be_hidden_by_default_when_instantiated(
        self, qt_application
    ) -> None:
        # isHidden() reflects explicit setVisible(False) regardless of parent state.
        bar = BottomBar()
        assert bar.translationIndicator.isHidden()

    def test_should_become_visible_when_show_translation_indicator_is_called(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.show_translation_indicator()
        assert not bar.translationIndicator.isHidden()

    def test_should_become_hidden_when_hide_translation_indicator_is_called(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.show_translation_indicator()
        bar.hide_translation_indicator()
        assert bar.translationIndicator.isHidden()

    def test_should_have_non_empty_text_in_indicator_when_instantiated(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        assert bar.translationIndicator.text() != ""

    def test_should_refresh_indicator_text_when_retranslate_ui_is_called(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.show_translation_indicator()
        # Simulate language change — text must remain non-empty.
        bar.retranslate_ui()
        assert bar.translationIndicator.text() != ""

    def test_should_preserve_indicator_visibility_when_retranslate_ui_is_called(
        self, qt_application
    ) -> None:
        bar = BottomBar()
        bar.show_translation_indicator()
        bar.retranslate_ui()
        # retranslate_ui must not hide the indicator.
        assert not bar.translationIndicator.isHidden()

    def test_should_connect_to_translation_manager_signals_when_wired(
        self, qt_application
    ) -> None:
        """Verify signal/slot wiring: manager signals control indicator visibility."""
        from ezqt_app.services.translation.manager import TranslationManager

        bar = BottomBar()
        manager = TranslationManager()

        manager.translation_started.connect(bar.show_translation_indicator)
        manager.translation_finished.connect(bar.hide_translation_indicator)

        manager._increment_pending()
        assert not bar.translationIndicator.isHidden()

        manager._decrement_pending()
        assert bar.translationIndicator.isHidden()
