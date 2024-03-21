from datetime import datetime
import sys
from pathlib import Path
from typing import Optional, Dict
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHeaderView
from PySide6.QtCore import Signal
from PySide6.QtGui import (
    QResizeEvent,
    QStandardItemModel,
    QStandardItem,
)


# Add the parent directory of 'src' to sys.path
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent.parent  # Adjust according to your project structure
sys.path.append(str(parent_dir))


# UI imports
from src.ui.welcome_ui import Ui_MainWindow  # noqa: E402


# Core imports
from src.core.project_creation_dialog import ProjectCreationDialog  # noqa: E402
from src.core.project_opening_dialog import ProjectOpeningDialog  # noqa: E402
from src.core.settings import (  # noqa: E402
    load_settings,
    load_themes,
    load_current_theme,
    get_recent_project_paths,
    load_ui,
    update_image,
)
from src.core.videoeditor import VideoEditorWindow  # noqa: E402

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
        self.ui = load_ui(
            main_window=self,
            ui=Ui_MainWindow(),
            settings=self.settings,
            current_theme=self.current_theme,
            themes=self.themes,
        )
        # Populate the recent projects list with the 10 latest projects
        self.populate_recent_projects()
        self.ui.recentProjectsTableView.doubleClicked.connect(
            lambda: self.open_project_from_list(
                self.ui.recentProjectsTableView.selectedIndexes()[0]
            )
        )

    @logger.catch
    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resize event for the main window"""
        super().resizeEvent(event)
        update_image(ui=self.ui, current_theme=self.current_theme)
        self.update_table_view()

    @logger.catch
    def update_table_view(self) -> None:
        """Update the table view based on the theme and resize event."""
        # Resize to fit the window, expand if needed
        self.ui.recentProjectsTableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    @logger.catch
    def populate_recent_projects(self):
        # Create a model with 3 columns
        model = QStandardItemModel(0, 3, self)
        model.setHorizontalHeaderLabels(["Project Path", "Last Modified", "Size"])

        for project in get_recent_project_paths():
            # Convert the last_modified timestamp to a human-readable format
            last_modified_date = datetime.fromtimestamp(
                project["last_modified"]
            ).strftime("%Y-%m-%d %H:%M:%S")
            # Format the size in a more readable format, e.g., in KB, MB
            size_kb = project["size"] / 1024  # Convert size to KB
            if size_kb < 1024:
                size_str = f"{size_kb:.2f} KB"
            else:
                size_mb = size_kb / 1024
                size_str = f"{size_mb:.2f} MB"

            # Create items for each column
            path_item = QStandardItem(project["path"])
            modified_item = QStandardItem(last_modified_date)
            size_item = QStandardItem(size_str)

            # Append the row to the model
            model.appendRow([path_item, modified_item, size_item])

        # Set the model to the table view
        self.ui.recentProjectsTableView.setModel(model)
        # Resize columns to fit content
        self.ui.recentProjectsTableView.resizeColumnsToContents()

    @logger.catch
    def open_project_from_list(self, index):
        # Retrieve the project path from the model item at the clicked index
        model = self.ui.recentProjectsTableView.model()
        project_path = model.data(
            model.index(index.row(), 0)
        )  # Assuming the project path is in the first column
        # Now you can call the method to open the project
        self.open_video_editor(project_path)

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
            self.videoEditor = VideoEditorWindow(self)

            # Change window title as current project name with file path
            self.videoEditor.setWindowTitle(f"Manim Studio - {project_file_path}")

            # Emit the signal after VideoEditor dialog is opened
            self.videoEditorOpened.emit(project_file_path)

            self.close()

            self.videoEditor.show()
        except Exception as e:
            logger.error(f"Error opening video editor: {e}cd")
        pass


if __name__ == "__main__":
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    widget = Main()
    widget.show()
    sys.exit(app.exec())
