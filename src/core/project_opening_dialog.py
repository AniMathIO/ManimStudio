import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Signal


# Add the parent directory of 'src' to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent.parent  # Adjust according to your project structure
sys.path.append(str(parent_dir))


from src.ui.project_opening_dialog_ui import Ui_Form as Ui_ProjectOpeningDialog
from settings import getRecentProjectPaths, addRecentProjectPath

from src.utils.logger_utility import logger


class ProjectOpeningDialog(QDialog):
    """Dialog for opening an existing project"""

    projectSelected = Signal(str)

    @logger.catch
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.ui = Ui_ProjectOpeningDialog()
        self.ui.setupUi(self)
        self.loadRecentProjects()

        self.ui.openProjectPushButton.clicked.connect(self.openProject)
        self.ui.projectSelectComboBox.mouseDoubleClickEvent = self.browseForProject

    @logger.catch
    def loadRecentProjects(self):
        """Load the recent projects into the combo box"""
        recentProjects = getRecentProjectPaths()
        for projectPath in recentProjects:
            self.ui.projectSelectComboBox.addItem(projectPath)

    @logger.catch
    def browseForProject(self, event):
        """Browse for a project"""
        projectPath, _ = QFileDialog.getOpenFileName(
            self, "Select Project", "", "Manim Studio Projects (*.mstp)"
        )
        if projectPath:
            self.projectSelected.emit(projectPath)
            addRecentProjectPath(projectPath)
            self.accept()

    @logger.catch
    def openProject(self):
        """Open the selected project"""
        selectedProject = self.ui.projectSelectComboBox.currentText()
        self.projectSelected.emit(selectedProject)
        self.accept()
