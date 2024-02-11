import os
import sys
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
)
from PySide6.QtCore import QFile, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap

# Add the parent directory of 'src' to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent.parent  # Adjust according to your project structure
sys.path.append(str(parent_dir))


from settings import (
    load_settings,
    load_themes,
    load_current_theme,
    update_settings,
)

# UI imports
from src.ui.settings_ui import Ui_Form

# Core imports
from src.core.project_creation_dialog import ProjectCreationDialog


class Main(QWidget):
    """Main class for the application"""

    styleSheetUpdated = Signal(str)

    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.customStyleSheet = ""
        self.settings = load_settings()
        self.themes = load_themes()
        self.current_theme = load_current_theme()

        self.load_ui()

    def apply_stylesheet(self):
        # Set the custom stylesheet based on the current theme
        self.customStyleSheet = f"background-color: {self.current_theme['background']}; color: {self.current_theme['font']}; border-color: {self.current_theme['primary']}; font-size: {self.settings['fontSize']}px; font-family: {self.settings['fontFamily']}; "
        self.setStyleSheet(self.customStyleSheet)

        # Check the theme name and update the image
        if (
            "latte" in self.current_theme["name"].lower()
            or "light" in self.current_theme["name"].lower()
        ):
            image_path = "docs/_static/ManimStudioLogoLight.png"
        else:
            image_path = "docs/_static/ManimStudioLogoDark.png"

        self.ui.label.setPixmap(QPixmap(image_path))

        self.styleSheetUpdated.emit(self.customStyleSheet)

    def load_ui(self):
        """Load the UI from the .ui file"""
        loader = QUiLoader()

        path = Path(__file__).resolve().parent.parent / "ui" / "form.ui"
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Apply the theme
        self.apply_stylesheet()

        self.ui.settingsBtn.clicked.connect(self.open_settings_dialog)
        self.ui.newProjectBtn.clicked.connect(self.showProjectCreationDialog)

    def open_settings_dialog(self):
        """Open the settings dialog"""
        self.settingsDialog = QDialog()
        self.uiSettings = Ui_Form()
        self.uiSettings.setupUi(self.settingsDialog)

        # Inherit the theme from the main window
        self.settingsDialog.setStyleSheet(self.customStyleSheet)
        self.styleSheetUpdated.connect(self.settingsDialog.setStyleSheet)

        # Load settings and themes to the dialog
        self.uiSettings.fontSizeSpinBox.setValue(self.settings["fontSize"])
        self.uiSettings.fontComboBox.setCurrentText(self.settings["fontFamily"])

        self.uiSettings.themeComboBox.clear()

        # Populate the theme combobox with full theme data
        for theme_module in self.themes:
            for variant in theme_module["variants"]:
                variant_data = json.dumps(variant)
                self.uiSettings.themeComboBox.addItem(variant["name"], variant_data)

        # Set the current theme in the combobox
        current_theme_index = self.uiSettings.themeComboBox.findText(
            self.current_theme["name"]
        )
        if current_theme_index >= 0:
            self.uiSettings.themeComboBox.setCurrentIndex(current_theme_index)

        self.uiSettings.saveSettingsBtn.clicked.connect(
            self.update_settings_from_dialog
        )

        self.settingsDialog.exec()

    def update_settings_from_dialog(self):
        """Update the settings from the dialog, and update the UI"""

        # Get recentProjects array from the current settings
        recentProjects = self.settings.get("recentProjects", [])

        # Get the current values from the dialog
        fontSize = self.uiSettings.fontSizeSpinBox.value()
        fontFamily = self.uiSettings.fontComboBox.currentText()

        # Extract full theme data from the selected item in the combobox
        theme_data_json = self.uiSettings.themeComboBox.currentData()
        selected_theme = json.loads(theme_data_json)

        # Create a new settings object
        new_settings = {
            "fontSize": fontSize,
            "fontFamily": fontFamily,
            "theme": selected_theme,
            "recentProjects": recentProjects,
        }

        # Pass the new settings to the settings module
        if update_settings(new_settings):
            # Update the global settings variable
            self.settings = new_settings
            # Update the current theme
            self.current_theme = load_current_theme()
            # Apply the stylesheet
            self.apply_stylesheet()

    def showProjectCreationDialog(self):
        try:
            dialog = ProjectCreationDialog(self)
            dialog.projectCreated.connect(
                self.openVideoEditor
            )  # Connect to the new method
            if dialog.exec():
                pass
        except Exception as e:
            print(f"Error showing project creation dialog: {e}")

    def openVideoEditor(self, projectFilePath):
        # Logic to open and initialize VideoEditor UI with the project file
        pass


if __name__ == "__main__":
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    widget = Main()
    widget.show()
    sys.exit(app.exec())
