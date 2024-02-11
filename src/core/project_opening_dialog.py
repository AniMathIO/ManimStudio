import os
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Signal
from src.ui.project_opening_dialog_ui import Ui_Form as Ui_ProjectOpeningDialog
from settings import getRecentProjectPaths, addRecentProjectPath


class ProjectOpeningDialog(QDialog):
    projectSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectOpeningDialog()
        self.ui.setupUi(self)
        self.loadRecentProjects()

        self.ui.openProjectPushButton.clicked.connect(self.openProject)
        self.ui.projectSelectComboBox.mouseDoubleClickEvent = self.browseForProject

    def loadRecentProjects(self):
        recentProjects = getRecentProjectPaths()
        for projectPath in recentProjects:
            self.ui.projectSelectComboBox.addItem(projectPath)

    def browseForProject(self, event):
        projectPath, _ = QFileDialog.getOpenFileName(
            self, "Select Project", "", "Manim Studio Projects (*.mstp)"
        )
        if projectPath:
            self.projectSelected.emit(projectPath)
            addRecentProjectPath(projectPath)
            self.accept()

    def openProject(self, event):
        selectedProject = self.ui.projectSelectComboBox.currentText()
        self.projectSelected.emit(selectedProject)
        self.accept()
