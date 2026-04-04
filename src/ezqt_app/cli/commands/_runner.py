# ///////////////////////////////////////////////////////////////
# CLI.RUNNER - Project template manager
# Project: ezqt_app
# ///////////////////////////////////////////////////////////////

"""Handles project creation, template management, and example generation."""

from __future__ import annotations

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////
# Standard library imports
import os
from pathlib import Path
from typing import Any

# Third-party imports
import click

# Local imports
from ezqt_app.utils.diagnostics import warn_tech


# ///////////////////////////////////////////////////////////////
# CLASSES
# ///////////////////////////////////////////////////////////////
class ProjectRunner:
    """Handles EzQt_App project operations and template management."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = Path.cwd()

    def get_project_info(self) -> dict[str, Any]:
        """Get information about the current project structure."""
        info = {
            "status": "unknown",
            "has_assets": False,
            "has_qrc": False,
            "has_bin": False,
            "has_config": False,
            "has_main": False,
            "has_tests": False,
        }

        assets_dir = self.project_root / "assets"
        bin_dir = self.project_root / "bin"
        qrc_file = bin_dir / "resources.qrc"
        legacy_qrc_file = self.project_root / "base_resources.qrc"
        app_config_file = bin_dir / "config" / "app.config.yaml"
        main_file = self.project_root / "main.py"
        tests_dir = self.project_root / "tests"

        if assets_dir.exists():
            info["has_assets"] = True
        if bin_dir.exists():
            info["has_bin"] = True
        if qrc_file.exists() or legacy_qrc_file.exists():
            info["has_qrc"] = True
        if app_config_file.exists():
            info["has_config"] = True
        if main_file.exists():
            info["has_main"] = True
        if tests_dir.exists():
            info["has_tests"] = True

        if all([info["has_bin"], info["has_qrc"], info["has_main"]]):
            info["status"] = "initialized"
        elif any(
            [
                info["has_bin"],
                info["has_qrc"],
                info["has_main"],
                info["has_assets"],
            ]
        ):
            info["status"] = "partial"
        else:
            info["status"] = "not_initialized"

        return info

    def create_project_template(
        self, template_type: str | None, project_name: str | None
    ) -> bool:
        """Create a new project with a predefined template."""
        if not template_type:
            template_type = "basic"

        if not project_name:
            project_name = "my_ezqt_app"

        if self.verbose:
            click.echo(f"Creating {template_type} template: {project_name}")

        try:
            project_dir = self.project_root / project_name
            if project_dir.exists():
                if not click.confirm(
                    f"Directory {project_name} already exists. Overwrite?"
                ):
                    return False
                import shutil

                shutil.rmtree(project_dir)

            project_dir.mkdir(parents=True)

            original_cwd = os.getcwd()
            os.chdir(project_dir)

            try:
                self._create_basic_template(project_name)

                if template_type == "advanced":
                    self._create_advanced_template(project_name)

                click.echo(f"Project '{project_name}' created successfully!")
                click.echo(f"Location: {project_dir.absolute()}")
                click.echo("\nNext steps:")
                click.echo(f"  cd {project_name}")
                click.echo("  python main.py")

                return True

            finally:
                os.chdir(original_cwd)

        except Exception as e:
            warn_tech(
                "cli.runner.create_project_template_failed",
                "Project template creation workflow failed",
                error=e,
            )
            if self.verbose:
                click.echo(f"Error creating template: {e}")
            return False

    def _create_basic_template(self, project_name: str) -> None:
        """Create basic project template."""
        if self.verbose:
            click.echo("Creating basic template...")

        (Path.cwd() / "assets").mkdir(exist_ok=True)
        (Path.cwd() / "assets" / "icons").mkdir(exist_ok=True)
        (Path.cwd() / "assets" / "images").mkdir(exist_ok=True)
        (Path.cwd() / "assets" / "themes").mkdir(exist_ok=True)

        main_content = f'''# -*- coding: utf-8 -*-
"""
{project_name} - Basic EzQt_App Application

A simple application using the EzQt_App framework.
"""

import sys

from ezqt_app import EzApplication, EzQt_App, init


def main():
    """Main application entry point."""
    init()

    app = EzApplication(sys.argv)
    window = EzQt_App()

    window.add_menu("Home", "home")
    window.add_menu("Settings", "settings")

    window.show()
    app.exec()


if __name__ == "__main__":
    main()
'''

        with open("main.py", "w", encoding="utf-8") as f:
            f.write(main_content)

        theme_content = """/* Basic Theme for EzQt_App */

QMainWindow {
    background-color: #2d2d2d;
    color: #ffffff;
}

QMenuBar {
    background-color: #3d3d3d;
    border-bottom: 1px solid #555555;
}

QPushButton {
    background-color: #0078d4;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    color: white;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QLabel {
    color: #ffffff;
    font-size: 14px;
}
"""

        with open("assets/themes/main_theme.qss", "w", encoding="utf-8") as f:
            f.write(theme_content)

        readme_content = f"""# {project_name}

A basic EzQt_App application.

## Quick Start

```bash
python main.py
```

## Structure

```
{project_name}/
├── main.py
├── assets/
│   ├── icons/
│   ├── images/
│   └── themes/
└── README.md
```

## Documentation

For more information, visit the [EzQt_App documentation](https://github.com/neuraaak/ezqt_app).
"""

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

    def _create_advanced_template(self, project_name: str) -> None:
        """Create advanced project template with additional features."""
        if self.verbose:
            click.echo("Creating advanced template...")

        (Path.cwd() / "src").mkdir(exist_ok=True)
        (Path.cwd() / "src" / "widgets").mkdir(exist_ok=True)
        (Path.cwd() / "src" / "utils").mkdir(exist_ok=True)
        (Path.cwd() / "tests").mkdir(exist_ok=True)
        (Path.cwd() / "docs").mkdir(exist_ok=True)

        advanced_main_content = f'''# -*- coding: utf-8 -*-
"""
{project_name} - Advanced EzQt_App Application

An advanced application using the EzQt_App framework with custom widgets
and advanced features.
"""

import sys

from ezqt_app import EzApplication, EzQt_App, init
from ezqt_app.services.translation import tr

from src.widgets.custom_widget import CustomWidget


class AdvancedApplication:
    """Advanced application class with custom functionality."""

    def __init__(self):
        """Initialize the advanced application."""
        init()

        self.app = EzApplication(sys.argv)
        self.window = EzQt_App()

        self.setup_application()

    def setup_application(self):
        """Setup the application with custom features."""
        self.home_page = self.window.add_menu("Home", "home")
        self.dashboard_page = self.window.add_menu("Dashboard", "chart")
        self.settings_page = self.window.add_menu("Settings", "settings")
        self.help_page = self.window.add_menu("Help", "help")

        self.setup_home_page()
        self.setup_dashboard_page()
        self.setup_settings_page()

        self.window.set_credits("Made with EzQt_App")
        self.window.set_version("1.0.0")

    def setup_home_page(self):
        """Setup the home page with custom widgets."""
        custom_widget = CustomWidget()
        self.home_page.layout().addWidget(custom_widget)

    def setup_dashboard_page(self):
        """Setup the dashboard page."""

    def setup_settings_page(self):
        """Setup the settings page."""

    def run(self):
        """Run the application."""
        self.window.show()
        return self.app.exec()


def main():
    """Main application entry point."""
    app = AdvancedApplication()
    return app.run()


if __name__ == "__main__":
    main()
'''

        with open("main.py", "w", encoding="utf-8") as f:
            f.write(advanced_main_content)

        custom_widget_content = '''# -*- coding: utf-8 -*-
"""
Custom Widget Module

Example custom widget for the advanced template.
"""

from PySide6.QtCore import QCoreApplication, QEvent, Qt
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout

from ezqt_app.utils.printer import get_printer


class CustomWidget(QFrame):
    """Example custom widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.retranslate_ui()

    def setup_ui(self):
        """Setup the user interface."""
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)

        layout = QVBoxLayout(self)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin: 10px;"
        )
        layout.addWidget(self.title_label)

        self.desc_label = QLabel()
        self.desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.desc_label)

        self.action_button = QPushButton()
        self.action_button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.action_button)

    def retranslate_ui(self):
        """Apply current translations to all owned text."""
        self.title_label.setText(
            QCoreApplication.translate("CustomWidget", "Custom Widget Title")
        )
        self.desc_label.setText(
            QCoreApplication.translate("CustomWidget", "This is a custom widget example")
        )
        self.action_button.setText(
            QCoreApplication.translate("CustomWidget", "Click Me")
        )

    def changeEvent(self, event):
        """Handle language change events."""
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    def on_button_clicked(self):
        """Handle button click event."""
        get_printer().info("Custom widget button clicked!")
'''

        with open("src/widgets/custom_widget.py", "w", encoding="utf-8") as f:
            f.write(custom_widget_content)

        test_content = '''# -*- coding: utf-8 -*-
"""
Test module for the advanced application.

Run with: python -m pytest tests/
"""

import pytest

from src.widgets.custom_widget import CustomWidget


def test_custom_widget_creation():
    """Test that custom widget can be created."""
    widget = CustomWidget()
    assert widget is not None
    assert widget.title_label is not None
    assert widget.action_button is not None


def test_custom_widget_button_click():
    """Test button click functionality."""
    widget = CustomWidget()
    assert widget.action_button is not None
'''

        with open("tests/test_custom_widget.py", "w", encoding="utf-8") as f:
            f.write(test_content)

    def list_available_templates(self) -> None:
        """List all available project templates."""
        templates = {
            "basic": "Simple EzQt_App project with basic structure",
            "advanced": "Advanced project with custom widgets and utilities",
        }

        click.echo("Available project templates:")
        click.echo("=" * 50)

        for template, description in templates.items():
            click.echo(f"  {template:<12} - {description}")

        click.echo("\nUsage: ezqt create --template <template> --name <project_name>")


# ///////////////////////////////////////////////////////////////
# MODULE-LEVEL HELPERS
# ///////////////////////////////////////////////////////////////
def create_project_template(
    template_type: str, project_name: str, verbose: bool = False
) -> bool:
    """Create a project template."""
    runner = ProjectRunner(verbose)
    return runner.create_project_template(template_type, project_name)


def get_project_info() -> dict[str, Any]:
    """Get current project information."""
    runner = ProjectRunner()
    return runner.get_project_info()


def list_available_templates() -> None:
    """List available templates."""
    runner = ProjectRunner()
    runner.list_available_templates()


# ///////////////////////////////////////////////////////////////
# PUBLIC API
# ///////////////////////////////////////////////////////////////
__all__ = [
    "ProjectRunner",
    "create_project_template",
    "get_project_info",
    "list_available_templates",
]
