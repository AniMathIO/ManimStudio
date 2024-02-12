import os
import sys
import dill
from pathlib import Path
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Signal

# Add the parent directory of 'src' to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent.parent  # Adjust according to your project structure
sys.path.append(str(parent_dir))

from src.ui.project_creation_dialog_ui import Ui_Form as Ui_ProjectCreationDialog
from src.core.settings import (
    addRecentProjectPath,
    addRecentProjectCreationPath,
    getRecentProjectCreationPaths,
)

from src.utils.logger_utility import logger


class ProjectCreationDialog(QDialog):
    """Dialog for creating a new project"""

    projectCreated = Signal(str)

    @logger.catch
    def __init__(self, parent=None):
        """Initializer"""
        super(ProjectCreationDialog, self).__init__(parent)
        self.ui = Ui_ProjectCreationDialog()
        self.ui.setupUi(self)
        self.loadRecentProjectPaths()
        self.ui.folderSelectComboBox.mouseDoubleClickEvent = self.selectFolder
        self.ui.createProjectPushButton.clicked.connect(self.createProject)

    @logger.catch
    def loadRecentProjectPaths(self):
        """Load the recent project paths into the combo box"""
        recentPaths = getRecentProjectCreationPaths()
        for path in recentPaths:
            self.ui.folderSelectComboBox.addItem(path)

    @logger.catch
    def selectFolder(self, event):
        """Select a folder for the project"""
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.ui.folderSelectComboBox.addItem(folder)

    @logger.catch
    def createProject(self):
        """Create a new project and emit the projectCreated signal"""
        projectName = self.ui.projectNameLineEdit.text()
        projectFolder = self.ui.folderSelectComboBox.currentText()
        if not projectName or not projectFolder:
            # Show an error message
            QMessageBox.critical(
                self, "Error", "Please enter a project name and select a folder"
            )
            logger.error("Project name or folder not entered")
            return

        projectPath = os.path.join(projectFolder, projectName)
        os.makedirs(projectPath, exist_ok=True)  # Create project directory

        initialState = {}  # Define your initial state here
        with open(os.path.join(projectPath, f"{projectName}.mstp"), "wb") as file:
            dill.dump(initialState, file)  # Serialize initial state

        self.projectCreated.emit(
            os.path.join(projectPath, f"{projectName}.mstp")
        )  # Emit signal with project file path

        addRecentProjectCreationPath(
            projectFolder
        )  # Update your settings with the new path

        addRecentProjectPath(os.path.join(projectPath, f"{projectName}.mstp"))

        # Close the dialog and optionally proceed to open the project in the editor
        self.accept()
