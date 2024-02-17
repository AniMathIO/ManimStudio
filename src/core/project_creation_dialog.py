import os
import sys
import dill
from pathlib import Path
from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox, QWidget
from PySide6.QtCore import Signal, QEvent


# UI imports
from src.ui.project_creation_dialog_ui import Ui_Form as Ui_ProjectCreationDialog

# Core imports
from src.core.settings import (
    add_recent_project_path,
    add_recent_project_creation_path,
    get_recent_project_creation_paths,
)

# Utils imports
from src.utils.logger_utility import logger

# Add the parent directory of 'src' to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent.parent  # Adjust according to your project structure
sys.path.append(str(parent_dir))


class ProjectCreationDialog(QDialog):
    """Dialog for creating a new project"""

    projectCreated = Signal(str)

    @logger.catch
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initializer"""
        super(ProjectCreationDialog, self).__init__(parent)
        self.ui: Ui_ProjectCreationDialog = Ui_ProjectCreationDialog()
        self.ui.setupUi(self)
        self.loadRecentProjectPaths()
        self.ui.folderSelectComboBox.mouseDoubleClickEvent = self.selectFolder
        self.ui.createProjectPushButton.clicked.connect(self.createProject)

    @logger.catch
    def loadRecentProjectPaths(self) -> None:
        """Load the recent project paths into the combo box"""
        recentPaths: List[str] = get_recent_project_creation_paths()
        for path in recentPaths:
            self.ui.folderSelectComboBox.addItem(path)

    @logger.catch
    def selectFolder(self, event: Optional[QEvent] = None) -> None:
        """Select a folder for the project"""
        folder: str = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.ui.folderSelectComboBox.addItem(folder)

    @logger.catch
    def createProject(self) -> None:
        """Create a new project and emit the projectCreated signal"""
        projectName: str = self.ui.projectNameLineEdit.text()
        projectFolder: str = self.ui.folderSelectComboBox.currentText()
        if not projectName or not projectFolder:
            # Show an error message
            QMessageBox.critical(
                self, "Error", "Please enter a project name and select a folder"
            )
            logger.error("Project name or folder not entered")
            return

        projectPath: str = os.path.join(projectFolder, projectName)
        os.makedirs(projectPath, exist_ok=True)  # Create project directory

        initialState: Dict[Any, Any] = {}  # Define your initial state here
        with open(os.path.join(projectPath, f"{projectName}.mstp"), "wb") as file:
            dill.dump(initialState, file)  # Serialize initial state

        self.projectCreated.emit(
            os.path.join(projectPath, f"{projectName}.mstp")
        )  # Emit signal with project file path

        add_recent_project_creation_path(
            projectFolder
        )  # Update your settings with the new path

        add_recent_project_path(os.path.join(projectPath, f"{projectName}.mstp"))

        # Close the dialog and optionally proceed to open the project in the editor
        self.accept()
