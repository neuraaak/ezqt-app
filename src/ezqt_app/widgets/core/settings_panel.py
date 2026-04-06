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
from typing import Any, cast

from pydantic import BaseModel, ConfigDict, ValidationError

# Third-party imports
from PySide6.QtCore import QEvent, QSize, Qt, Signal
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
from ...utils.diagnostics import warn_tech


# ///////////////////////////////////////////////////////////////
# PYDANTIC SCHEMAS
# ///////////////////////////////////////////////////////////////
class _SettingsPanelOptionSchema(BaseModel):
    """Schema for one settings panel option."""

    model_config = ConfigDict(extra="forbid")

    type: str = "text"
    label: str | None = None
    description: str = ""
    default: Any = None
    enabled: bool = True
    options: list[str] = []
    min: int | None = None
    max: int | None = None
    unit: str | None = None


class _SettingsPanelConfigSchema(BaseModel):
    """Schema for the settings_panel section in app config."""

    model_config = ConfigDict(extra="forbid")

    app: dict[str, Any] | None = None
    settings_panel: dict[str, _SettingsPanelOptionSchema] = {}


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class SettingsPanel(QFrame):
    """
    This class is used to create a settings panel.
    It contains a top border, a content settings frame and a theme settings container.
    The settings panel is used to display the settings.
    """

    # Signal emitted when a setting changes
    settingChanged = Signal(str, object)  # key, value
    # Signal emitted when language changes
    languageChanged = Signal()

    # ///////////////////////////////////////////////////////////////

    def _settings_storage_prefix(self) -> list[str]:
        """Return config keys (file name + nested path) used to persist setting values."""
        config_name = "app"
        try:
            from ...services.config import get_config_service

            app_config = get_config_service().load_config(config_name)
            app_section = app_config.get("app", {})
            root = str(app_section.get("settings_storage_root", "settings_panel"))
            parts = [part for part in root.split(".") if part]

            def _exists(path_parts: list[str]) -> bool:
                current: object = app_config
                for part in path_parts:
                    if not isinstance(current, dict) or part not in current:
                        return False
                    current = current[part]
                return isinstance(current, dict)

            if parts and _exists(parts):
                return [config_name, *parts]
        except Exception as e:
            warn_tech(
                code="widgets.settings_panel.storage_prefix_resolution_failed",
                message="Could not resolve settings storage prefix from app config",
                error=e,
            )
        return [config_name, "settings_panel"]

    def _sync_theme_selector_with_settings(self) -> None:
        """Align theme selector UI with the currently active settings theme."""
        try:
            if not hasattr(self, "_theme_selector"):
                return

            theme_selector = self._theme_selector
            gui = get_settings_service().gui
            current_internal = f"{gui.THEME_PRESET}:{gui.THEME}"
            current_display = self._theme_value_to_display.get(current_internal, "")

            if current_display and hasattr(theme_selector, "set_value"):
                theme_selector.set_value(current_display)
        except Exception as e:
            warn_tech(
                code="widgets.settings_panel.theme_selector_sync_failed",
                message="Could not synchronize theme selector with active settings",
                error=e,
            )

    def __init__(
        self,
        parent: QWidget | None = None,
        width: int = 240,
        load_from_yaml: bool = True,
    ) -> None:
        super().__init__(parent)
        self._widgets: list[QWidget] = []
        self._settings: dict[str, Any] = {}

        # Store configuration
        self._width = width

        self.setObjectName("settings_panel")
        self.setMinimumSize(QSize(0, 0))
        self.setMaximumSize(QSize(0, 16777215))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)

        # ////// SETUP MAIN LAYOUT
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setObjectName("settings_layout")
        self._layout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP TOP BORDER
        self._top_border = QFrame(self)
        self._top_border.setObjectName("settings_top_border")
        self._top_border.setMaximumSize(QSize(16777215, 3))
        self._top_border.setFrameShape(QFrame.Shape.NoFrame)
        self._top_border.setFrameShadow(QFrame.Shadow.Raised)
        self._layout.addWidget(self._top_border)

        # ////// SETUP SCROLL AREA
        self._scroll_area = QScrollArea(self)
        self._scroll_area.setObjectName("settings_scroll_area")
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll_area.setFrameShadow(QFrame.Shadow.Raised)
        self._layout.addWidget(self._scroll_area)

        # ////// SETUP CONTENT WIDGET
        self._content_widget = QFrame()
        self._content_widget.setObjectName("content_widget")
        self._content_widget.setFrameShape(QFrame.Shape.NoFrame)
        self._content_widget.setFrameShadow(QFrame.Shadow.Raised)
        self._content_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self._scroll_area.setWidget(self._content_widget)

        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setObjectName("content_layout")
        self._content_layout.setSpacing(0)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ////// SETUP THEME SECTION
        self._theme_section_frame = QFrame(self._content_widget)
        self._theme_section_frame.setObjectName("theme_section_frame")
        self._theme_section_frame.setFrameShape(QFrame.Shape.NoFrame)
        self._theme_section_frame.setFrameShadow(QFrame.Shadow.Raised)
        self._content_layout.addWidget(
            self._theme_section_frame, 0, Qt.AlignmentFlag.AlignTop
        )

        self._theme_section_layout = QVBoxLayout(self._theme_section_frame)
        self._theme_section_layout.setSpacing(8)
        self._theme_section_layout.setObjectName("theme_section_layout")
        self._theme_section_layout.setContentsMargins(10, 10, 10, 10)

        # Build theme options from palette (display label → internal value mapping).
        from ...services.ui.theme_service import ThemeService

        _theme_options_data = ThemeService.get_available_themes()
        self._theme_options_map: dict[str, str] = dict(_theme_options_data)
        self._theme_value_to_display: dict[str, str] = {
            v: d for d, v in _theme_options_data
        }

        _gui = get_settings_service().gui
        _current_internal = f"{_gui.THEME_PRESET}:{_gui.THEME}"
        _current_display = self._theme_value_to_display.get(
            _current_internal,
            _theme_options_data[0][0] if _theme_options_data else "",
        )

        from ...widgets.extended.setting_widgets import SettingSelect

        self._theme_selector = SettingSelect(
            label="Active Theme",
            description="",
            options=[d for d, _ in _theme_options_data],
            default=_current_display,
        )
        self._theme_selector.setObjectName("theme_selector")
        self._theme_selector.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self._widgets.append(self._theme_selector)
        self._theme_selector.valueChanged.connect(
            lambda _key, display_val: self._on_theme_selector_changed(display_val)
        )
        self._theme_section_layout.addWidget(self._theme_selector)

        if load_from_yaml:
            self.load_settings_from_yaml()

        self.settingChanged.connect(self._on_setting_changed)

    # ///////////////////////////////////////////////////////////////

    def load_settings_from_yaml(self) -> None:
        """Load settings from YAML file."""
        try:
            from ...services.config import get_config_service

            app_config = get_config_service().load_config("app", force_reload=True)
            if not isinstance(app_config, dict):
                app_config = {}

            validated = _SettingsPanelConfigSchema.model_validate(app_config)

            for key, config_model in validated.settings_panel.items():
                if key == "theme":
                    continue

                if config_model.enabled:
                    config = config_model.model_dump(mode="python", exclude_none=True)
                    widget = self.add_setting_from_config(key, config)
                    default_value = config_model.default
                    if default_value is not None and hasattr(widget, "set_value"):
                        cast(Any, widget).set_value(default_value)

        except ValidationError as e:
            warn_tech(
                code="widgets.settings_panel.load_yaml_validation_failed",
                message="Invalid settings panel configuration payload",
                error=e,
            )
        except Exception as e:
            warn_tech(
                code="widgets.settings_panel.load_yaml_failed",
                message="Error loading settings from YAML",
                error=e,
            )

    def add_setting_from_config(self, key: str, config: dict) -> QWidget:
        """Add a setting based on its YAML configuration."""
        setting_type = config.get("type", "text")
        label = config.get("label", key)
        description = config.get("description", "")
        default_value = config.get("default")

        setting_container = QFrame(self._content_widget)
        setting_container.setObjectName(f"setting_container_{key}")
        setting_container.setFrameShape(QFrame.Shape.NoFrame)
        setting_container.setFrameShadow(QFrame.Shadow.Raised)

        container_layout = QVBoxLayout(setting_container)
        container_layout.setSpacing(8)
        container_layout.setObjectName(f"setting_container_layout_{key}")
        container_layout.setContentsMargins(10, 10, 10, 10)

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
        else:
            widget = self._create_text_widget(
                label,
                description,
                str(default_value) if default_value is not None else "",
                key,
            )

        container_layout.addWidget(widget)
        self._content_layout.addWidget(setting_container)
        self._settings[key] = widget

        return widget

    def _create_toggle_widget(
        self, label: str, description: str, default: bool, key: str | None = None
    ) -> QWidget:
        """Create a toggle widget with label and description."""
        from ...widgets.extended.setting_widgets import SettingToggle

        widget = SettingToggle(label, description, default)
        if key:
            widget.set_key(key)
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
            widget.set_key(key)
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
            widget.set_key(key)
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_checkbox_widget(
        self, label: str, description: str, default: bool, key: str | None = None
    ) -> QWidget:
        """Create a checkbox widget with label and description."""
        from ...widgets.extended.setting_widgets import SettingCheckbox

        widget = SettingCheckbox(label, description, default)
        if key:
            widget.set_key(key)
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_text_widget(
        self, label: str, description: str, default: str, key: str | None = None
    ) -> QWidget:
        """Create a text widget with label and description."""
        from ...widgets.extended.setting_widgets import SettingText

        widget = SettingText(label, description, default)
        if key:
            widget.set_key(key)
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    # ///////////////////////////////////////////////////////////////

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
        widget.set_key(key)
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
        widget.set_key(key)
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
        widget.set_key(key)
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
        widget.set_key(key)
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
        widget.set_key(key)
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def _on_setting_changed(self, key: str, value):
        """Called when a setting changes."""
        if not hasattr(self, "_processing_setting_change"):
            self._processing_setting_change = False

        if self._processing_setting_change:
            return

        self._processing_setting_change = True

        try:
            try:
                from ...services.application.app_service import AppService

                AppService.stage_config_value(
                    [*self._settings_storage_prefix(), key, "default"], value
                )
            except Exception as e:
                warn_tech(
                    code="widgets.settings_panel.save_setting_failed",
                    message=f"Could not save setting '{key}' to YAML",
                    error=e,
                )

            if key == "language":
                try:
                    translation_service = get_translation_service()
                    current_lang = translation_service.get_current_language_name()
                    if current_lang != str(value):
                        translation_service.change_language(str(value))
                        self._sync_theme_selector_with_settings()
                        self.languageChanged.emit()
                except Exception as e:
                    warn_tech(
                        code="widgets.settings_panel.change_language_failed",
                        message="Could not change language",
                        error=e,
                    )

            self.settingChanged.emit(key, value)
        finally:
            self._processing_setting_change = False

    # ///////////////////////////////////////////////////////////////

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
        """Stage all current setting values."""
        from ...services.application.app_service import AppService

        for key, widget in self._settings.items():
            try:
                AppService.stage_config_value(
                    [*self._settings_storage_prefix(), key, "default"],
                    widget.get_value(),
                )
            except Exception as e:
                warn_tech(
                    code="widgets.settings_panel.save_all_settings_failed",
                    message=f"Could not save setting '{key}' to YAML",
                    error=e,
                )

    def retranslate_ui(self) -> None:
        """Apply current translations to all owned text labels."""
        if hasattr(self, "_theme_selector") and hasattr(
            self._theme_selector, "retranslate_ui"
        ):
            self._theme_selector.retranslate_ui()
        for widget in self._settings.values():
            if hasattr(widget, "retranslate_ui"):
                widget.retranslate_ui()

    def changeEvent(self, event: QEvent) -> None:
        """Handle Qt change events."""
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    # ///////////////////////////////////////////////////////////////

    def get_width(self) -> int:
        """Get panel width."""
        return self._width

    def set_width(self, width: int) -> None:
        """Set panel width."""
        self._width = width

    def get_theme_selector(self):
        """Get the theme selector if available."""
        if hasattr(self, "_theme_selector"):
            return self._theme_selector
        return None

    def update_all_theme_icons(self) -> None:
        """Update theme icons for all widgets that support it."""
        current_theme = get_settings_service().gui.THEME
        for widget in self._widgets:
            # New pattern: widgets exposing setTheme(theme) directly
            setter = getattr(widget, "setTheme", None)
            if callable(setter):
                setter(current_theme)
                continue
            # Legacy pattern: widgets exposing update_theme_icon()
            updater = getattr(widget, "update_theme_icon", None)
            if callable(updater):
                updater()

        self.style().unpolish(self)
        self.style().polish(self)

        for child in self.findChildren(QWidget):
            child.style().unpolish(child)
            child.style().polish(child)

    def _on_theme_selector_changed(self, display_value: str) -> None:
        """Called when the theme selector value changes.

        ``display_value`` is the human-readable label emitted by the select
        widget (e.g. ``"Blue Gray - Dark"``).  It is converted to the internal
        ``"preset:variant"`` format before being persisted and broadcast.
        """
        try:
            internal_value = self._theme_options_map.get(display_value, display_value)
            from ...services.application.app_service import AppService
            from ...services.settings import get_settings_service

            get_settings_service().set_theme(internal_value)
            AppService.stage_config_value(
                [*self._settings_storage_prefix(), "theme", "default"],
                internal_value,
            )
            self.settingChanged.emit("theme", internal_value)
        except Exception as e:
            warn_tech(
                code="widgets.settings_panel.theme_selector_change_failed",
                message="Could not handle theme selector change",
                error=e,
            )

    def add_setting_widget(self, widget: QWidget) -> None:
        """Add a new setting widget to the settings panel."""
        setting_container = QFrame(self._content_widget)
        setting_container.setObjectName(f"setting_container_{widget.objectName()}")
        setting_container.setFrameShape(QFrame.Shape.NoFrame)
        setting_container.setFrameShadow(QFrame.Shadow.Raised)

        container_layout = QVBoxLayout(setting_container)
        container_layout.setSpacing(8)
        container_layout.setObjectName(
            f"setting_container_layout_{widget.objectName()}"
        )
        container_layout.setContentsMargins(10, 10, 10, 10)

        container_layout.addWidget(widget)
        self._content_layout.addWidget(setting_container)
        self._widgets.append(widget)

    def add_setting_section(self, title: str = "") -> QFrame:
        """Add a new settings section with optional title."""
        section = QFrame(self._content_widget)
        section.setObjectName(f"settings_section_{title.replace(' ', '_').lower()}")
        section.setFrameShape(QFrame.Shape.NoFrame)
        section.setFrameShadow(QFrame.Shadow.Raised)

        section_layout = QVBoxLayout(section)
        section_layout.setSpacing(8)
        section_layout.setObjectName(
            f"settings_section_layout_{title.replace(' ', '_').lower()}"
        )
        section_layout.setContentsMargins(10, 10, 10, 10)

        if title:
            title_label = QLabel(title, section)
            title_label.setObjectName(
                f"settings_section_title_{title.replace(' ', '_').lower()}"
            )
            if Fonts.SEGOE_UI_10_REG is not None:
                title_label.setFont(Fonts.SEGOE_UI_10_REG)
            title_label.setAlignment(
                Qt.AlignmentFlag.AlignLeading
                | Qt.AlignmentFlag.AlignLeft
                | Qt.AlignmentFlag.AlignVCenter
            )
            section_layout.addWidget(title_label)

        self._content_layout.addWidget(section)
        return section

    def scroll_to_top(self) -> None:
        """Scroll to top of settings panel."""
        if hasattr(self, "_scroll_area"):
            self._scroll_area.verticalScrollBar().setValue(0)

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of settings panel."""
        if hasattr(self, "_scroll_area"):
            scrollbar = self._scroll_area.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def scroll_to_widget(self, widget: QWidget) -> None:
        """Scroll to a specific widget in the settings panel."""
        if hasattr(self, "_scroll_area") and widget:
            widget_pos = widget.mapTo(self._content_widget, widget.rect().topLeft())
            self._scroll_area.verticalScrollBar().setValue(widget_pos.y())


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = ["SettingsPanel"]
