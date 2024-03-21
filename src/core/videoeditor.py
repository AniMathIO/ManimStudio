from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal

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
