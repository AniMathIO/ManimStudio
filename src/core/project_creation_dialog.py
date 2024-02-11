import os
import sys
from pathlib import Path
import dill
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Signal

# Add the parent directory of 'src' to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent.parent  # Adjust according to your project structure
sys.path.append(str(parent_dir))

from src.ui.project_creation_dialog_ui import Ui_Form as Ui_ProjectCreationDialog
from src.core.settings import addRecentProjectPath, getRecentProjectPaths


class ProjectCreationDialog(QDialog):
    projectCreated = Signal(str)

    def __init__(self, parent=None):
        super(ProjectCreationDialog, self).__init__(parent)
        self.ui = Ui_ProjectCreationDialog()
        self.ui.setupUi(self)
        self.loadRecentProjectPaths()
        self.ui.folderSelectComboBox.mouseDoubleClickEvent = self.selectFolder
        self.ui.createProjectPushButton.clicked.connect(self.createProject)

    def loadRecentProjectPaths(self):
        recentPaths = getRecentProjectPaths()
        for path in recentPaths:
            self.ui.folderSelectComboBox.addItem(path)

    def selectFolder(self, event):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.ui.folderSelectComboBox.addItem(folder)

    def createProject(self):
        projectName = self.ui.projectNameLineEdit.text()
        projectFolder = self.ui.folderSelectComboBox.currentText()
        if not projectName or not projectFolder:
            # Show an error message
            QMessageBox.critical(
                self, "Error", "Please enter a project name and select a folder"
            )
            return

        projectPath = os.path.join(projectFolder, projectName)
        os.makedirs(projectPath, exist_ok=True)  # Create project directory

        initialState = {}  # Define your initial state here
        with open(os.path.join(projectPath, f"{projectName}.mstp"), "wb") as file:
            dill.dump(initialState, file)  # Serialize initial state

        self.projectCreated.emit(
            os.path.join(projectPath, f"{projectName}.mstp")
        )  # Emit signal with project file path

        addRecentProjectPath(projectFolder)  # Update your settings with the new path

        # Close the dialog and optionally proceed to open the project in the editor
        self.accept()
