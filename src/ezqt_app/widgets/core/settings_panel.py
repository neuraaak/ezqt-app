# ///////////////////////////////////////////////////////////////
# WIDGETS.CORE.SETTINGS_PANEL - Settings panel widget
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""SettingsPanel widget with scrollable settings and YAML persistence."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import contextlib
from typing import Any

# Third-party imports
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

# Local imports
from ...services.settings import get_settings_service
from ...services.translation import get_translation_service
from ...services.ui import Fonts
from ...utils.printer import get_printer


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class SettingsPanel(QFrame):
    """
    This class is used to create a settings panel.
    It contains a top border, a content settings frame and a theme settings container.
    The settings panel is used to display the settings.
    """

    _widgets: list = []  # Type hint removed to avoid circular import
    _settings: dict[str, Any] = {}  # Settings storage

    # Signal emitted when a setting changes
    settingChanged = Signal(str, object)  # key, value
    # Signal emitted when language changes
    languageChanged = Signal()

    # ///////////////////////////////////////////////////////////////

    def __init__(
        self,
        parent: QWidget | None = None,
        width: int = 240,
        load_from_yaml: bool = True,
    ) -> None:
        super().__init__(parent)

        # ///////////////////////////////////////////////////////////////
        # Store configuration
        self._width = width

        self.setObjectName("settingsPanel")
        self.setMinimumSize(QSize(0, 0))
        self.setMaximumSize(QSize(0, 16777215))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)
        # //////
        self.VL_settingsPanel = QVBoxLayout(self)
        self.VL_settingsPanel.setSpacing(0)
        self.VL_settingsPanel.setObjectName("VL_settingsPanel")
        self.VL_settingsPanel.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////

        self.settingsTopBorder = QFrame(self)
        self.settingsTopBorder.setObjectName("settingsTopBorder")
        self.settingsTopBorder.setMaximumSize(QSize(16777215, 3))
        self.settingsTopBorder.setFrameShape(QFrame.Shape.NoFrame)
        self.settingsTopBorder.setFrameShadow(QFrame.Shadow.Raised)
        #
        self.VL_settingsPanel.addWidget(self.settingsTopBorder)

        # ///////////////////////////////////////////////////////////////

        # Create QScrollArea for settings
        self.settingsScrollArea = QScrollArea(self)
        self.settingsScrollArea.setObjectName("settingsScrollArea")
        self.settingsScrollArea.setWidgetResizable(True)
        self.settingsScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.settingsScrollArea.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.settingsScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.settingsScrollArea.setFrameShadow(QFrame.Shadow.Raised)
        #
        self.VL_settingsPanel.addWidget(self.settingsScrollArea)

        # ///////////////////////////////////////////////////////////////

        # Container widget for all settings
        self.contentSettings = QFrame()
        self.contentSettings.setObjectName("contentSettings")
        self.contentSettings.setFrameShape(QFrame.Shape.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Shadow.Raised)
        self.contentSettings.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        #
        self.settingsScrollArea.setWidget(self.contentSettings)
        # //////
        self.VL_contentSettings = QVBoxLayout(self.contentSettings)
        self.VL_contentSettings.setObjectName("VL_contentSettings")
        self.VL_contentSettings.setSpacing(0)
        self.VL_contentSettings.setContentsMargins(0, 0, 0, 0)
        self.VL_contentSettings.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ///////////////////////////////////////////////////////////////

        self.themeSettingsContainer = QFrame(self.contentSettings)
        self.themeSettingsContainer.setObjectName("themeSettingsContainer")
        self.themeSettingsContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.themeSettingsContainer.setFrameShadow(QFrame.Shadow.Raised)
        #
        self.VL_contentSettings.addWidget(
            self.themeSettingsContainer, 0, Qt.AlignmentFlag.AlignTop
        )
        # //////
        self.VL_themeSettingsContainer = QVBoxLayout(self.themeSettingsContainer)
        self.VL_themeSettingsContainer.setSpacing(8)
        self.VL_themeSettingsContainer.setObjectName("VL_themeSettingsContainer")
        self.VL_themeSettingsContainer.setContentsMargins(10, 10, 10, 10)

        # ///////////////////////////////////////////////////////////////

        self.themeLabel = QLabel("Active Theme", self.themeSettingsContainer)
        self.themeLabel.setObjectName("themeLabel")
        if Fonts.SEGOE_UI_10_SB is not None:
            self.themeLabel.setFont(Fonts.SEGOE_UI_10_SB)
        self.themeLabel.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        #
        self.VL_themeSettingsContainer.addWidget(self.themeLabel)

        # ///////////////////////////////////////////////////////////////

        # Create theme selector if OptionSelector is available
        try:
            from ezqt_widgets import OptionSelector

            # Create theme selector with correct signature
            # OptionSelector expects: items, default_id, min_width, min_height, orientation, animation_duration, parent
            self.themeToggleButton = OptionSelector(
                items=["Light", "Dark"],  # List of options
                default_id=1,  # 0 = Light, 1 = Dark (Dark by default)
                min_width=None,
                min_height=None,
                orientation="horizontal",
                animation_duration=get_settings_service().gui.TIME_ANIMATION,
                parent=self.themeSettingsContainer,
            )
            self.themeToggleButton.setObjectName("themeToggleButton")
            self.themeToggleButton.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
            )
            self.themeToggleButton.setFixedHeight(40)
            self._widgets.append(self.themeToggleButton)

            # Connect theme selector change signal
            self._connect_theme_selector_signals()

            # Add to layout
            self.VL_themeSettingsContainer.addWidget(self.themeToggleButton)

        except ImportError:
            get_printer().warning(
                "OptionSelector not available, theme toggle not created"
            )

        # ///////////////////////////////////////////////////////////////
        # Automatic loading from YAML if requested
        if load_from_yaml:
            self.load_settings_from_yaml()

        # Connect setting changes
        self.settingChanged.connect(self._on_setting_changed)

    # ///////////////////////////////////////////////////////////////

    def load_settings_from_yaml(self) -> None:
        """Load settings from YAML file."""
        try:
            from pathlib import Path

            import yaml

            # Try to load the full app.yaml file directly
            # Try multiple possible paths
            possible_paths = [
                Path.cwd() / "bin" / "config" / "app.yaml",  # User project
                Path(__file__).parent.parent.parent
                / "resources"
                / "config"
                / "app.yaml",  # Package
            ]

            app_config = None
            for path in possible_paths:
                if path.exists():
                    with open(path, encoding="utf-8") as f:
                        app_config = yaml.safe_load(f)
                    break

            if app_config is None:
                get_printer().warning("Could not find app.yaml file")
                return

            # Extract settings_panel section
            settings_config = app_config.get("settings_panel", {})

            # Create widgets for each setting
            for key, config in settings_config.items():
                # Exclude theme as it's already manually managed by OptionSelector
                if key == "theme":
                    continue

                if config.get("enabled", True):  # Check if setting is enabled
                    widget = self.add_setting_from_config(key, config)

                    # Use default value from config (which may have been updated)
                    default_value = config.get("default")
                    if default_value is not None and hasattr(widget, "set_value"):
                        widget.set_value(default_value)  # type: ignore[union-attr]

        except Exception as e:
            get_printer().warning(f"Error loading settings from YAML: {e}")

    def add_setting_from_config(self, key: str, config: dict) -> QWidget:
        """Add a setting based on its YAML configuration."""
        setting_type = config.get("type", "text")
        label = config.get("label", key)
        description = config.get("description", "")
        default_value = config.get("default")

        # Create container for this setting (like themeSettingsContainer)
        setting_container = QFrame(self.contentSettings)
        setting_container.setObjectName(f"settingContainer_{key}")
        setting_container.setFrameShape(QFrame.Shape.NoFrame)
        setting_container.setFrameShadow(QFrame.Shadow.Raised)

        # Container layout with margins
        container_layout = QVBoxLayout(setting_container)
        container_layout.setSpacing(8)
        container_layout.setObjectName(f"VL_settingContainer_{key}")
        container_layout.setContentsMargins(10, 10, 10, 10)

        # Create widget based on type
        if setting_type == "toggle":
            widget = self._create_toggle_widget(
                label,
                description,
                bool(default_value) if default_value is not None else False,
                key,
            )
        elif setting_type == "select":
            options = config.get("options", [])
            widget = self._create_select_widget(
                label,
                description,
                options,
                str(default_value) if default_value is not None else "",
                key,
            )
        elif setting_type == "slider":
            min_val = config.get("min", 0)
            max_val = config.get("max", 100)
            unit = config.get("unit", "")
            widget = self._create_slider_widget(
                label,
                description,
                min_val,
                max_val,
                int(default_value) if default_value is not None else 0,
                unit,
                key,
            )
        elif setting_type == "checkbox":
            widget = self._create_checkbox_widget(
                label,
                description,
                bool(default_value) if default_value is not None else False,
                key,
            )
        else:  # text by default
            widget = self._create_text_widget(
                label,
                description,
                str(default_value) if default_value is not None else "",
                key,
            )

        # Add widget to container
        container_layout.addWidget(widget)

        # Add container to main layout
        self.VL_contentSettings.addWidget(setting_container)

        # Store reference
        self._settings[key] = widget

        return widget

    def _create_toggle_widget(
        self, label: str, description: str, default: bool, key: str | None = None
    ) -> QWidget:
        """Create a toggle widget with label and description."""
        from ...widgets.extended.setting_widgets import SettingToggle

        widget = SettingToggle(label, description, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_select_widget(
        self,
        label: str,
        description: str,
        options: list[str],
        default: str,
        key: str | None = None,
    ) -> QWidget:
        """Create a select widget with label and description."""
        from ...widgets.extended.setting_widgets import SettingSelect

        widget = SettingSelect(label, description, options, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_slider_widget(
        self,
        label: str,
        description: str,
        min_val: int,
        max_val: int,
        default: int,
        unit: str,
        key: str | None = None,
    ) -> QWidget:
        """Create a slider widget with label and description."""
        from ...widgets.extended.setting_widgets import SettingSlider

        widget = SettingSlider(label, description, min_val, max_val, default, unit)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_checkbox_widget(
        self, label: str, description: str, default: bool, key: str | None = None
    ) -> QWidget:
        """Create a checkbox widget with label and description."""
        from ...widgets.extended.setting_widgets import SettingCheckbox

        widget = SettingCheckbox(label, description, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_text_widget(
        self, label: str, description: str, default: str, key: str | None = None
    ) -> QWidget:
        """Create a text widget with label and description."""
        from ...widgets.extended.setting_widgets import SettingText

        widget = SettingText(label, description, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    # ///////////////////////////////////////////////////////////////
    # Simplified methods for manual setting addition

    def add_toggle_setting(
        self,
        key: str,
        label: str,
        default: bool = False,
        description: str = "",
        enabled: bool = True,  # noqa: ARG002
    ):
        """Add a toggle setting."""
        from ...widgets.extended.setting_widgets import SettingToggle

        widget = SettingToggle(label, description, default)
        widget._key = key  # Set the key
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def add_select_setting(
        self,
        key: str,
        label: str,
        options: list[str],
        default: str | None = None,
        description: str = "",
        enabled: bool = True,  # noqa: ARG002
    ):
        """Add a selection setting."""
        from ...widgets.extended.setting_widgets import SettingSelect

        widget = SettingSelect(label, description, options, default)
        widget._key = key  # Set the key
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def add_slider_setting(
        self,
        key: str,
        label: str,
        min_val: int,
        max_val: int,
        default: int,
        unit: str = "",
        description: str = "",
        enabled: bool = True,  # noqa: ARG002
    ):
        """Add a slider setting."""
        from ...widgets.extended.setting_widgets import SettingSlider

        widget = SettingSlider(label, description, min_val, max_val, default, unit)
        widget._key = key  # Set the key
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def add_text_setting(
        self,
        key: str,
        label: str,
        default: str = "",
        description: str = "",
        enabled: bool = True,  # noqa: ARG002
    ):
        """Add a text setting."""
        from ...widgets.extended.setting_widgets import SettingText

        widget = SettingText(label, description, default)
        widget._key = key  # Set the key
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def add_checkbox_setting(
        self,
        key: str,
        label: str,
        default: bool = False,
        description: str = "",
        enabled: bool = True,  # noqa: ARG002
    ):
        """Add a checkbox setting."""
        from ...widgets.extended.setting_widgets import SettingCheckbox

        widget = SettingCheckbox(label, description, default)
        widget._key = key  # Set the key
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def _on_setting_changed(self, key: str, value):
        """Called when a setting changes."""
        # Protection against recursion
        if not hasattr(self, "_processing_setting_change"):
            self._processing_setting_change = False

        if self._processing_setting_change:
            return  # Avoid recursion

        self._processing_setting_change = True

        try:
            # Save to YAML
            try:
                # Direct import to avoid circular import
                from ...services.application.app_service import AppService as Kernel

                # Save directly to settings_panel[key].default
                Kernel.write_yaml_config(["settings_panel", key, "default"], value)
            except Exception as e:
                get_printer().warning(f"Could not save setting '{key}' to YAML: {e}")

            # Special handling for language changes
            if key == "language":
                try:
                    translation_service = get_translation_service()
                    # Check if language really changes
                    current_lang = translation_service.get_current_language_name()
                    if current_lang != str(value):
                        translation_service.change_language(str(value))
                        # Emit language change signal
                        self.languageChanged.emit()
                except Exception as e:
                    get_printer().warning(f"Could not change language: {e}")

            # Emit signal for application
            self.settingChanged.emit(key, value)
        finally:
            self._processing_setting_change = False

    # ///////////////////////////////////////////////////////////////
    # Utility methods

    def get_setting_value(self, key: str) -> Any:
        """Get the value of a setting."""
        if key in self._settings:
            return self._settings[key].get_value()
        return None

    def set_setting_value(self, key: str, value: Any) -> None:
        """Set the value of a setting."""
        if key in self._settings:
            self._settings[key].set_value(value)

    def get_all_settings(self) -> dict[str, Any]:
        """Get all settings and their values."""
        return {key: widget.get_value() for key, widget in self._settings.items()}

    def save_all_settings_to_yaml(self) -> None:
        """Save all settings to YAML file."""
        # Direct import to avoid circular import
        from ...services.application.app_service import AppService as Kernel

        for key, widget in self._settings.items():
            try:
                Kernel.write_yaml_config(
                    ["settings_panel", key, "default"], widget.get_value()
                )
            except Exception as e:
                get_printer().warning(f"Could not save setting '{key}' to YAML: {e}")

    # ///////////////////////////////////////////////////////////////
    # Panel management methods

    def get_width(self) -> int:
        """Get panel width."""
        return self._width

    def set_width(self, width: int) -> None:
        """Set panel width."""
        self._width = width

    def get_theme_toggle_button(self):
        """Get the theme toggle button if available."""
        if hasattr(self, "themeToggleButton"):
            return self.themeToggleButton
        return None

    def update_all_theme_icons(self) -> None:
        """Update theme icons for all widgets that support it."""
        for widget in self._widgets:
            if hasattr(widget, "update_theme_icon"):
                widget.update_theme_icon()

        # Force refresh of settings panel style
        self.style().unpolish(self)
        self.style().polish(self)

        # Also refresh all child widgets
        for child in self.findChildren(QWidget):
            child.style().unpolish(child)
            child.style().polish(child)

    def _connect_theme_selector_signals(self) -> None:
        """Connect theme selector signals."""
        with contextlib.suppress(Exception):
            if hasattr(self, "themeToggleButton"):
                # Connect OptionSelector valueChanged signal
                theme_button = self.themeToggleButton

                if hasattr(theme_button, "valueChanged"):
                    theme_button.valueChanged.connect(self._on_theme_selector_changed)
                elif hasattr(theme_button, "clicked"):
                    theme_button.clicked.connect(self._on_theme_selector_clicked)

    def _on_theme_selector_changed(self, value):
        """Called when theme selector value changes."""
        try:
            # OptionSelector.value already returns "Light" or "Dark"
            english_value = value.lower()

            # Save English value to YAML
            from ...services.application.app_service import AppService as Kernel

            Kernel.write_yaml_config(
                ["settings_panel", "theme", "default"], english_value
            )

            # Emit signal with English value
            self.settingChanged.emit("theme", english_value)

        except Exception as e:
            get_printer().warning(f"Could not handle theme selector change: {e}")

    def _on_theme_selector_clicked(self):
        """Called when theme selector is clicked."""
        try:
            if hasattr(self, "themeToggleButton"):
                # Get text value directly
                current_value = self.themeToggleButton.value.lower()

                # Save English value to YAML
                from ...services.application.app_service import AppService as Kernel

                Kernel.write_yaml_config(
                    ["settings_panel", "theme", "default"], current_value
                )

                # Emit signal with English value
                self.settingChanged.emit("theme", current_value)

        except Exception as e:
            get_printer().warning(f"Could not handle theme selector click: {e}")

    def update_theme_selector_items(self) -> None:
        """Update theme selector items with translations."""
        with contextlib.suppress(Exception):
            if hasattr(self, "themeToggleButton"):
                from ...services.translation import tr

                # Translate items for display
                translated_items = [tr("Light"), tr("Dark")]

                # Save current value (ID)
                theme_button = self.themeToggleButton
                current_id = (
                    theme_button.value_id if hasattr(theme_button, "value_id") else 0
                )

                # Update widget texts directly
                if hasattr(theme_button, "_options"):
                    for i, (_option_id, option_widget) in enumerate(
                        theme_button._options.items()
                    ):
                        if i < len(translated_items):
                            if hasattr(option_widget, "label"):
                                option_widget.label.setText(
                                    translated_items[i].capitalize()
                                )
                            elif hasattr(option_widget, "setText"):
                                option_widget.setText(translated_items[i].capitalize())

                # Reapply current ID to maintain selection
                if hasattr(theme_button, "value_id") and hasattr(
                    theme_button, "_value_id"
                ):
                    theme_button._value_id = current_id
                    # Force selector movement
                    if current_id in theme_button._options:
                        theme_button.move_selector(theme_button._options[current_id])

    def add_setting_widget(self, widget: QWidget) -> None:
        """Add a new setting widget to the settings panel."""
        # Create container for setting (like themeSettingsContainer)
        setting_container = QFrame(self.contentSettings)
        setting_container.setObjectName(f"settingContainer_{widget.objectName()}")
        setting_container.setFrameShape(QFrame.Shape.NoFrame)
        setting_container.setFrameShadow(QFrame.Shadow.Raised)

        # Container layout with margins (like VL_themeSettingsContainer)
        container_layout = QVBoxLayout(setting_container)
        container_layout.setSpacing(8)
        container_layout.setContentsMargins(10, 10, 10, 10)

        # Add widget to container
        container_layout.addWidget(widget)

        # Add container to main layout
        self.VL_contentSettings.addWidget(setting_container)
        self._widgets.append(widget)

    def add_setting_section(self, title: str = "") -> QFrame:
        """Add a new settings section with optional title."""
        section = QFrame(self.contentSettings)
        section.setObjectName(f"settingsSection_{title.replace(' ', '_')}")
        section.setFrameShape(QFrame.Shape.NoFrame)
        section.setFrameShadow(QFrame.Shadow.Raised)

        section_layout = QVBoxLayout(section)
        section_layout.setSpacing(8)
        section_layout.setContentsMargins(10, 10, 10, 10)

        if title:
            title_label = QLabel(title, section)
            if Fonts.SEGOE_UI_10_REG is not None:
                title_label.setFont(Fonts.SEGOE_UI_10_REG)
            title_label.setAlignment(
                Qt.AlignmentFlag.AlignLeading
                | Qt.AlignmentFlag.AlignLeft
                | Qt.AlignmentFlag.AlignVCenter
            )
            section_layout.addWidget(title_label)

        self.VL_contentSettings.addWidget(section)
        return section

    def scroll_to_top(self) -> None:
        """Scroll to top of settings panel."""
        if hasattr(self, "settingsScrollArea"):
            self.settingsScrollArea.verticalScrollBar().setValue(0)

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of settings panel."""
        if hasattr(self, "settingsScrollArea"):
            scrollbar = self.settingsScrollArea.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def scroll_to_widget(self, widget: QWidget) -> None:
        """
        Scroll to a specific widget in the settings panel.

        Args:
            widget: The widget to scroll to
        """
        if hasattr(self, "settingsScrollArea") and widget:
            # Calculate widget position in scroll area
            widget_pos = widget.mapTo(self.contentSettings, widget.rect().topLeft())
            self.settingsScrollArea.verticalScrollBar().setValue(widget_pos.y())


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["SettingsPanel"]
