# ///////////////////////////////////////////////////////////////
# WIDGETS.EXTENDED.SETTING_WIDGETS - Settings widget components
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Setting widget components: toggle, select, slider, text, checkbox."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Third-party imports
from ezqt_widgets import ToggleSwitch
from PySide6.QtCore import QCoreApplication, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSlider,
    QVBoxLayout,
    QWidget,
)

# Local imports
from ...services.settings import get_settings_service


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class BaseSettingWidget(QWidget):
    """Base class for all setting widgets."""

    def __init__(self, label: str, description: str = ""):
        super().__init__()
        self._label_text = label
        self._description_text = description
        self._key = None
        self.setObjectName("base_setting_widget")

    def set_key(self, key: str):
        """Set the setting key."""
        self._key = key

    def _tr(self, text: str) -> str:
        """Shortcut for translation with global context."""
        return QCoreApplication.translate("EzQt_App", text)

    def retranslate_ui(self):
        """To be implemented by subclasses."""


class SettingToggle(BaseSettingWidget):
    """Widget for toggle settings (on/off)."""

    valueChanged = Signal(str, bool)

    def __init__(self, label: str, description: str = "", default: bool = False):
        super().__init__(label, description)
        self._value = default
        self.setObjectName("setting_toggle_container")
        self.setProperty("type", "setting_toggle")
        self._setup_ui()

    def _setup_ui(self):
        """Configure the user interface."""
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._control_layout = QHBoxLayout()
        self._control_layout.setSpacing(8)
        self._control_layout.setContentsMargins(0, 0, 0, 0)

        self._label_widget = QLabel(self._tr(self._label_text))
        self._label_widget.setObjectName("setting_label")
        self._label_widget.setWordWrap(True)
        self._control_layout.addWidget(self._label_widget, 1)

        animation_enabled = get_settings_service().gui.TIME_ANIMATION > 0
        self._control_widget = ToggleSwitch(animation=animation_enabled)
        self._control_widget.setObjectName("setting_toggle")
        self._control_widget.checked = self._value
        self._control_widget.toggled.connect(self._on_toggled)
        self._control_layout.addWidget(self._control_widget, 0)

        self._layout.addLayout(self._control_layout)

        self._description_label = None
        if self._description_text:
            self._description_label = QLabel(self._tr(self._description_text))
            self._description_label.setObjectName("setting_description")
            self._description_label.setWordWrap(True)
            self._layout.addWidget(self._description_label)

    def retranslate_ui(self):
        """Update strings after language change."""
        self._label_widget.setText(self._tr(self._label_text))
        if self._description_label:
            self._description_label.setText(self._tr(self._description_text))

    def _on_toggled(self, checked: bool):
        self._value = checked
        self.valueChanged.emit(self._key, checked)

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, val: bool):
        self._value = val
        self._control_widget.checked = val

    def get_value(self) -> bool:
        return self._value

    def set_value(self, val: bool):
        self._value = val
        self._control_widget.checked = val


class SettingSelect(BaseSettingWidget):
    """Widget for selection settings."""

    valueChanged = Signal(str, str)

    def __init__(
        self,
        label: str,
        description: str = "",
        options: list | None = None,
        default: str | None = None,
    ):
        super().__init__(label, description)
        self._options = options or []
        self._value = default or (options[0] if options else "")
        self.setObjectName("setting_select_container")
        self.setProperty("type", "setting_select")
        self._setup_ui()

    def _setup_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._label_widget = QLabel(self._tr(self._label_text))
        self._label_widget.setObjectName("setting_label")
        self._label_widget.setWordWrap(True)
        self._layout.addWidget(self._label_widget)

        self._control_widget = QComboBox()
        self._control_widget.setObjectName("setting_combo_box")
        self._control_widget.addItems(self._options)
        if self._value in self._options:
            self._control_widget.setCurrentText(self._value)
        self._control_widget.currentTextChanged.connect(self._on_text_changed)
        self._layout.addWidget(self._control_widget)

        self._description_label = None
        if self._description_text:
            self._description_label = QLabel(self._tr(self._description_text))
            self._description_label.setObjectName("setting_description")
            self._description_label.setWordWrap(True)
            self._layout.addWidget(self._description_label)

    def retranslate_ui(self):
        self._label_widget.setText(self._tr(self._label_text))
        if self._description_label:
            self._description_label.setText(self._tr(self._description_text))

    def _on_text_changed(self, text: str):
        self._value = text
        self.valueChanged.emit(self._key, text)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, val: str):
        self._value = val
        if val in self._options:
            self._control_widget.setCurrentText(val)

    def get_value(self) -> str:
        return self._value

    def set_value(self, val: str):
        self._value = val
        if val in self._options:
            self._control_widget.setCurrentText(val)


class SettingSlider(BaseSettingWidget):
    """Widget for numeric settings with slider."""

    valueChanged = Signal(str, int)

    def __init__(
        self,
        label: str,
        description: str = "",
        min_val: int = 0,
        max_val: int = 100,
        default: int = 50,
        unit: str = "",
    ):
        super().__init__(label, description)
        self._min_val = min_val
        self._max_val = max_val
        self._value = default
        self._unit = unit
        self.setObjectName("setting_slider_container")
        self.setProperty("type", "setting_slider")
        self._setup_ui()

    def _setup_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._header_layout = QHBoxLayout()
        self._header_layout.setSpacing(8)
        self._header_layout.setContentsMargins(0, 0, 0, 0)

        self._label_widget = QLabel(self._tr(self._label_text))
        self._label_widget.setObjectName("setting_label")
        self._label_widget.setWordWrap(True)
        self._header_layout.addWidget(self._label_widget, 1)

        self._value_label = QLabel(f"{self._value}{self._unit}")
        self._value_label.setObjectName("setting_value_label")
        self._header_layout.addWidget(self._value_label, 0)

        self._layout.addLayout(self._header_layout)

        self._control_widget = QSlider(Qt.Orientation.Horizontal)
        self._control_widget.setObjectName("setting_slider")
        self._control_widget.setMinimum(self._min_val)
        self._control_widget.setMaximum(self._max_val)
        self._control_widget.setValue(self._value)
        self._control_widget.valueChanged.connect(self._on_value_changed)
        self._layout.addWidget(self._control_widget)

        self._description_label = None
        if self._description_text:
            self._description_label = QLabel(self._tr(self._description_text))
            self._description_label.setObjectName("setting_description")
            self._description_label.setWordWrap(True)
            self._layout.addWidget(self._description_label)

    def retranslate_ui(self):
        self._label_widget.setText(self._tr(self._label_text))
        if self._description_label:
            self._description_label.setText(self._tr(self._description_text))

    def _on_value_changed(self, value: int):
        self._value = value
        self._value_label.setText(f"{value}{self._unit}")
        self.valueChanged.emit(self._key, value)

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int):
        self._value = val
        self._control_widget.setValue(val)
        self._value_label.setText(f"{val}{self._unit}")

    def get_value(self) -> int:
        return self._value

    def set_value(self, val: int):
        self._value = val
        self._control_widget.setValue(val)
        self._value_label.setText(f"{val}{self._unit}")


class SettingText(BaseSettingWidget):
    """Widget for text settings."""

    valueChanged = Signal(str, str)

    def __init__(self, label: str, description: str = "", default: str = ""):
        super().__init__(label, description)
        self._value = default
        self.setObjectName("setting_text_container")
        self.setProperty("type", "setting_text")
        self._setup_ui()

    def _setup_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._label_widget = QLabel(self._tr(self._label_text))
        self._label_widget.setObjectName("setting_label")
        self._label_widget.setWordWrap(True)
        self._layout.addWidget(self._label_widget)

        self._control_widget = QLineEdit()
        self._control_widget.setObjectName("setting_text_edit")
        self._control_widget.setText(self._value)
        self._control_widget.textChanged.connect(self._on_text_changed)
        self._layout.addWidget(self._control_widget)

        self._description_label = None
        if self._description_text:
            self._description_label = QLabel(self._tr(self._description_text))
            self._description_label.setObjectName("setting_description")
            self._description_label.setWordWrap(True)
            self._layout.addWidget(self._description_label)

    def retranslate_ui(self):
        self._label_widget.setText(self._tr(self._label_text))
        if self._description_label:
            self._description_label.setText(self._tr(self._description_text))

    def _on_text_changed(self, text: str):
        self._value = text
        self.valueChanged.emit(self._key, text)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, val: str):
        self._value = val
        self._control_widget.setText(val)

    def get_value(self) -> str:
        return self._value

    def set_value(self, val: str):
        self._value = val
        self._control_widget.setText(val)


class SettingCheckbox(BaseSettingWidget):
    """Widget for checkbox settings (on/off)."""

    valueChanged = Signal(str, bool)

    def __init__(self, label: str, description: str = "", default: bool = False):
        super().__init__(label, description)
        self._value = default
        self.setObjectName("setting_checkbox_container")
        self.setProperty("type", "setting_checkbox")
        self._setup_ui()

    def _setup_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._control_layout = QHBoxLayout()
        self._control_layout.setSpacing(8)
        self._control_layout.setContentsMargins(0, 0, 0, 0)

        self._label_widget = QLabel(self._tr(self._label_text))
        self._label_widget.setObjectName("setting_label")
        self._label_widget.setWordWrap(True)
        self._control_layout.addWidget(self._label_widget, 1)

        animation_enabled = get_settings_service().gui.TIME_ANIMATION > 0
        self._control_widget = ToggleSwitch(animation=animation_enabled)
        self._control_widget.setObjectName("setting_toggle")
        self._control_widget.checked = self._value
        self._control_widget.toggled.connect(self._on_toggled)
        self._control_layout.addWidget(self._control_widget, 0)

        self._layout.addLayout(self._control_layout)

        self._description_label = None
        if self._description_text:
            self._description_label = QLabel(self._tr(self._description_text))
            self._description_label.setObjectName("setting_description")
            self._description_label.setWordWrap(True)
            self._layout.addWidget(self._description_label)

    def retranslate_ui(self):
        self._label_widget.setText(self._tr(self._label_text))
        if self._description_label:
            self._description_label.setText(self._tr(self._description_text))

    def _on_toggled(self, checked: bool):
        self._value = checked
        self.valueChanged.emit(self._key, checked)

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, val: bool):
        self._value = val
        self._control_widget.checked = val

    def get_value(self) -> bool:
        return self._value

    def set_value(self, val: bool):
        self._value = val
        self._control_widget.checked = val


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "BaseSettingWidget",
    "SettingCheckbox",
    "SettingSelect",
    "SettingSlider",
    "SettingText",
    "SettingToggle",
]
