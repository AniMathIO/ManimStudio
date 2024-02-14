import sys
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QDialog,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSizePolicy


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
from src.ui.videoeditor_ui import Ui_Form as Ui_VideoEditor
from src.ui.form_ui import Ui_Main

# Core imports
from src.core.project_creation_dialog import ProjectCreationDialog
from src.core.project_opening_dialog import ProjectOpeningDialog

# Logger
from src.utils.logger_utility import logger


class Main(QWidget):
    """Main class for the application"""

    styleSheetUpdated = Signal(str)
    videoEditorOpened = Signal(str)

    @logger.catch
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.customStyleSheet = ""
        self.settings = load_settings()
        self.themes = load_themes()
        self.current_theme = load_current_theme()
        logger.info("Main window initialized")
        self.load_ui()

    @logger.catch
    def resizeEvent(self, event):
        """Resize event for the main window"""
        super().resizeEvent(event)
        self.update_image()

    @logger.catch
    def update_image(self):
        """Update the image based on the theme and resize event."""

        if (
            "latte" in self.current_theme["name"].lower()
            or "light" in self.current_theme["name"].lower()
        ):
            image_path = "docs/_static/ManimStudioLogoLight.png"
        else:
            image_path = "docs/_static/ManimStudioLogoDark.png"

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaledPixmap = pixmap.scaled(
                self.ui.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.ui.label.setPixmap(scaledPixmap)

        self.ui.label.setAlignment(Qt.AlignCenter)

    @logger.catch
    def apply_stylesheet(self):
        """Apply the stylesheet to the main window and update the image based on the theme"""

        # Set the custom stylesheet based on the current theme
        self.customStyleSheet = f"background-color: {self.current_theme['background']}; color: {self.current_theme['font']}; border-color: {self.current_theme['primary']}; font-size: {self.settings['fontSize']}px; font-family: {self.settings['fontFamily']}; "
        self.setStyleSheet(self.customStyleSheet)

        # Update the image
        self.update_image()

        self.styleSheetUpdated.emit(self.customStyleSheet)
        logger.info("Stylesheet applied")

    @logger.catch
    def load_ui(self):
        """Load the UI from the .ui file"""

        self.ui = Ui_Main()
        self.ui.setupUi(self)

        self.ui.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # Apply the theme
        self.apply_stylesheet()

        self.ui.settingsBtn.clicked.connect(self.open_settings_dialog)
        self.ui.newProjectBtn.clicked.connect(self.showProjectCreationDialog)
        self.ui.openProjectBtn.clicked.connect(self.showProjectOpenDialog)

        logger.info("UI loaded")

    @logger.catch
    def open_settings_dialog(self):
        """Open the settings dialog"""
        self.settingsDialog = QDialog()
        self.uiSettings = Ui_Form()
        self.uiSettings.setupUi(self.settingsDialog)

        # Change window title
        self.settingsDialog.setWindowTitle("Settings")

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

    @logger.catch
    def update_settings_from_dialog(self):
        """Update the settings from the dialog, and update the UI"""

        # Get recentProjects array from the current settings
        recentProjectPaths = self.settings.get("recentProjectPaths", [])

        # Get recentProjectCreationPaths array from the current settings
        recentProjectCreationPaths = self.settings.get("recentProjectCreationPaths", [])

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
            "recentProjectCreationPaths": recentProjectCreationPaths,
            "recentProjectPaths": recentProjectPaths,
        }

        # Pass the new settings to the settings module
        if update_settings(new_settings):
            # Update the global settings variable
            self.settings = new_settings
            # Update the current theme
            self.current_theme = load_current_theme()
            # Apply the stylesheet
            self.apply_stylesheet()

    @logger.catch
    def showProjectCreationDialog(self):
        """Show the project creation dialog"""
        try:
            dialog = ProjectCreationDialog(self)
            dialog.projectCreated.connect(
                self.openVideoEditor
            )  # Connect to the new method
            self.videoEditorOpened.connect(
                dialog.close
            )  # Close dialog when VideoEditor opens
            self.videoEditorOpened.connect(
                self.close
            )  # Close the main window (WelcomeScreen) as well

            if dialog.exec():
                pass
        except Exception as e:
            logger.error(f"Error showing project creation dialog: {e}")

    @logger.catch
    def showProjectOpenDialog(self):
        """Show the project open dialog"""
        try:
            dialog = ProjectOpeningDialog(self)
            dialog.projectSelected.connect(self.openVideoEditor)
            self.videoEditorOpened.connect(
                dialog.close
            )  # Close dialog when VideoEditor opens
            self.videoEditorOpened.connect(
                self.close
            )  # Close the main window (WelcomeScreen) as well
            dialog.exec()
        except Exception as e:
            logger.error(f"Error showing project open dialog: {e}")

    @logger.catch
    def openVideoEditor(self, projectFilePath):
        """Open the video editor with the project file"""
        try:
            self.videoEditor = QDialog()
            self.uiVideoEditor = Ui_VideoEditor()
            self.uiVideoEditor.setupUi(self.videoEditor)
            # Apply the theme
            self.videoEditor.setStyleSheet(self.customStyleSheet)
            # Change window title as current project name with file path
            self.videoEditor.setWindowTitle(f"Manim Studio - {projectFilePath}")

            # Emit the signal after VideoEditor dialog is opened
            self.videoEditorOpened.emit(projectFilePath)
            self.videoEditor.exec()
        except Exception as e:
            logger.error(f"Error opening video editor: {e}")
        pass


if __name__ == "__main__":
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    widget = Main()
    widget.show()
    sys.exit(app.exec())
