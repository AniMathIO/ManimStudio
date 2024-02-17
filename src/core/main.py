import sys
import json
from pathlib import Path
from typing import Optional, Dict, List
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QDialog,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QResizeEvent, QAction
from PySide6.QtWidgets import QSizePolicy

# Add the parent directory of 'src' to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent.parent  # Adjust according to your project structure
sys.path.append(str(parent_dir))


# UI imports
from src.ui.settings_ui import Ui_Form  # noqa: E402
from src.ui.videoeditor_ui import Ui_Form as Ui_VideoEditor  # noqa: E402
from src.ui.welcome_ui import Ui_MainWindow  # noqa: E402

# Core imports
from src.core.project_creation_dialog import ProjectCreationDialog  # noqa: E402
from src.core.project_opening_dialog import ProjectOpeningDialog  # noqa: E402
from src.core.settings import (  # noqa: E402
    load_settings,
    load_themes,
    load_current_theme,
    update_settings,
)

# Utils imports
from src.utils.logger_utility import logger  # noqa: E402


class Main(QMainWindow):
    """Main class for the application"""

    styleSheetUpdated = Signal(str)
    videoEditorOpened = Signal(str)

    @logger.catch
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initializer"""
        super().__init__(parent)
        self.customStyleSheet = ""
        self.settings: Dict = load_settings()
        self.themes: Dict = load_themes()
        self.current_theme: Dict = load_current_theme()
        logger.info("Main window initialized")
        self.load_ui()

    @logger.catch
    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resize event for the main window"""
        super().resizeEvent(event)
        self.update_image()

    @logger.catch
    def update_image(self) -> None:
        """Update the image based on the theme and resize event."""

        if (
            "latte" in self.current_theme["name"].lower()
            or "light" in self.current_theme["name"].lower()
        ):
            image_path: str = "docs/_static/ManimStudioLogoLight.png"
        else:
            image_path: str = "docs/_static/ManimStudioLogoDark.png"

        pixmap: QPixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaledPixmap: QPixmap = pixmap.scaled(
                self.ui.label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.ui.label.setPixmap(scaledPixmap)

        self.ui.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @logger.catch
    def apply_stylesheet(self) -> None:
        """Apply the stylesheet to the main window and update the image based on the theme"""

        # Set the custom stylesheet based on the current theme
        self.customStyleSheet: str = (
            f"background-color: {self.current_theme['background']}; color: {self.current_theme['font']}; border-color: {self.current_theme['primary']}; font-size: {self.settings['fontSize']}px; font-family: {self.settings['fontFamily']}; "
        )
        self.setStyleSheet(self.customStyleSheet)

        self.customMenubarStylesheet = str(
            f"background-color: {self.current_theme['primary']}; color: {self.current_theme['font']}; border-color: {self.current_theme['primary']}; font-size: {self.settings['fontSize']}px; font-family: {self.settings['fontFamily']}; "
        )
        self.ui.menubar.setStyleSheet(self.customMenubarStylesheet)

        # Update the image
        self.update_image()

        self.styleSheetUpdated.emit(self.customStyleSheet)
        logger.info("Stylesheet applied")

    @logger.catch
    def load_ui(self) -> None:
        """Load the UI from the .ui file"""

        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        )

        # Apply the theme
        self.apply_stylesheet()
        
        # Create new menubar item
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        self.ui.menubar.addAction(settings_action)

        self.ui.newProjectBtn.clicked.connect(self.show_project_creation_dialog)
        self.ui.openProjectBtn.clicked.connect(self.show_project_open_dialog)

        logger.info("UI loaded")

    @logger.catch
    def open_settings_dialog(self) -> None:
        """Open the settings dialog"""
        self.settingsDialog: QDialog = QDialog()
        self.uiSettings: Ui_Form = Ui_Form()
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
    def update_settings_from_dialog(self) -> None:
        """Update the settings from the dialog, and update the UI"""

        # Get recentProjects array from the current settings
        recentProjectPaths: List[str] = self.settings.get("recentProjectPaths", [])

        # Get recentProjectCreationPaths array from the current settings
        recentProjectCreationPaths: List[str] = self.settings.get(
            "recentProjectCreationPaths", []
        )

        # Get the current values from the dialog
        fontSize: int = self.uiSettings.fontSizeSpinBox.value()
        fontFamily: str = self.uiSettings.fontComboBox.currentText()

        # Extract full theme data from the selected item in the combobox
        theme_data_json: str = self.uiSettings.themeComboBox.currentData()
        selected_theme: Dict = json.loads(theme_data_json)

        # Create a new settings object
        new_settings: Dict = {
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
    def show_project_creation_dialog(self) -> None:
        """Show the project creation dialog"""
        try:
            dialog: ProjectCreationDialog = ProjectCreationDialog(self)
            dialog.projectCreated.connect(
                self.open_video_editor
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
    def show_project_open_dialog(self) -> None:
        """Show the project open dialog"""
        try:
            dialog: ProjectOpeningDialog = ProjectOpeningDialog(self)
            dialog.projectSelected.connect(self.open_video_editor)
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
    def open_video_editor(self, project_file_path: str) -> None:
        """Open the video editor with the project file"""
        try:
            self.videoEditor: QDialog = QDialog()
            self.uiVideoEditor: Ui_VideoEditor = Ui_VideoEditor()
            self.uiVideoEditor.setupUi(self.videoEditor)
            # Apply the theme
            self.videoEditor.setStyleSheet(self.customStyleSheet)
            # Change window title as current project name with file path
            self.videoEditor.setWindowTitle(f"Manim Studio - {project_file_path}")

            # Emit the signal after VideoEditor dialog is opened
            self.videoEditorOpened.emit(project_file_path)
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
