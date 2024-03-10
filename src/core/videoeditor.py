from PySide6.QtWidgets import QMainWindow, QWidget, QSizePolicy
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal, Qt

# UI imports
from src.ui.videoeditor_ui import Ui_Form as Ui_VideoEditor

# Core imports
from src.core.settings import (
    open_settings_dialog,
    load_settings,
    load_themes,
    load_current_theme,
    apply_stylesheet,
)
from src.core.timeline import Timeline

# Utils imports
from src.utils.logger_utility import logger


class VideoEditorWindow(QMainWindow):
    """Main window for the video editor application."""

    styleSheetUpdated = Signal(str)

    @logger.catch
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)

        self.central_widget = QWidget(self)
        self.ui = Ui_VideoEditor()
        self.ui.setupUi(self.central_widget)
        self.setCentralWidget(
            self.central_widget
        )  # Set the central widget of QMainWindow

        # Set resize policy
        self.central_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        self.ui.timelineVerticalLayout.setContentsMargins(0, 0, 0, 0)

        # Instantiate Timeline widget and add it to the QVBoxLayout
        self.timeline_widget = Timeline(parent=self.central_widget)
        self.ui.timelineVerticalLayout.addWidget(
            self.timeline_widget, alignment=Qt.AlignmentFlag.AlignLeft
        )  # Use the QVBoxLayout for timeline

        self.customStyleSheet = ""

        self.settings = load_settings()
        self.themes = load_themes()
        self.current_theme = load_current_theme()

        apply_stylesheet(self, self.ui, self.settings, self.current_theme)

        self.create_menubar()

    @logger.catch
    def create_menubar(self):
        """Create the menubar for the main window."""

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        self.menuBar().addAction(settings_action)

    @logger.catch
    def open_settings(self):
        """Open the settings dialog."""

        open_settings_dialog(self, self.settings, self.themes, self.current_theme)
