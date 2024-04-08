from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QSizePolicy,
    QApplication,
    QFileDialog,
    QListWidgetItem,
    QAbstractItemView,
    QMenu,
)
from PySide6.QtGui import QAction, QDropEvent
from PySide6.QtCore import Signal, Qt, QMimeData, QUrl
import os

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
from src.core.renderer import create_low_quality_version

# Utils imports
from src.utils.logger_utility import logger


class VideoEditorWindow(QMainWindow):
    """Main window for the video editor application."""

    styleSheetUpdated = Signal(str)

    @logger.catch
    def __init__(self, parent=None):
        """Initializer"""
        super().__init__(parent)
        self.isSettingsDialogOpen = False
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
        self.timeline_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,  # Allow horizontal expansion
            QSizePolicy.Policy.Preferred,  # Default vertical policy
        )
        self.ui.timelineVerticalLayout.addWidget(
            self.timeline_widget
        )  # Use the QVBoxLayout for timeline

        self.customStyleSheet = ""

        self.settings = load_settings()
        self.themes = load_themes()
        self.current_theme = load_current_theme()

        apply_stylesheet(self, self.ui, self.settings, self.current_theme)

        self.create_menubar()

        self.ui.videoPreviewSlider.valueChanged.connect(
            lambda value: self.timeline_widget.updateIndicatorPosition(
                value, self.ui.videoPreviewSlider.maximum()
            )
        )

        self.ui.libraryWidget.setDragEnabled(True)
        self.ui.libraryWidget.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.ui.libraryWidget.model().rowsInserted.connect(self.updateItemMimeData)

        self.ui.libraryWidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.ui.libraryWidget.customContextMenuRequested.connect(
            self.showListWidgetContextMenu
        )

    @logger.catch
    def showListWidgetContextMenu(self, position):
        item = self.ui.libraryWidget.itemAt(position)
        if item:
            contextMenu = QMenu(self)
            addToTimelineAction = contextMenu.addAction("Add to Timeline")
            addToTimelineAction.triggered.connect(lambda: self.addItemToTimeline(item))
            contextMenu.exec(self.ui.libraryWidget.mapToGlobal(position))

    @logger.catch
    def addItemToTimeline(self, item):
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.timeline_widget.addMediaToTimeline(file_path)

    @logger.catch
    def updateItemMimeData(self, parent, first, last):
        for row in range(first, last + 1):
            index = self.ui.libraryWidget.model().index(row, 0, parent)
            item = self.ui.libraryWidget.itemFromIndex(index)
            file_path = item.data(Qt.ItemDataRole.UserRole)
            mimeData = item.data(Qt.ItemDataRole.UserRole + 1)
            if not mimeData:
                mimeData = QMimeData()
                mimeData.setUrls([QUrl.fromLocalFile(file_path)])
                item.setData(Qt.ItemDataRole.UserRole + 1, mimeData)

    @logger.catch
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    @logger.catch
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            for url in urls:
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    self.handle_dropped_file(file_path)
        else:
            event.ignore()

    @logger.catch
    def handle_dropped_file(self, file_path):
        low_quality_path = create_low_quality_version(
            file_path, os.path.dirname(os.path.abspath(__file__))
        )
        if low_quality_path:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.ItemDataRole.UserRole, low_quality_path)
            self.ui.libraryWidget.addItem(item)

    @logger.catch
    def create_menubar(self):
        """Create the menubar for the main window."""

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        self.menuBar().addAction(settings_action)

    @logger.catch
    def open_settings(self):
        """Open the settings dialog."""
        self.isSettingsDialogOpen = True
        logger.info("Opening settings dialog.")
        open_settings_dialog(self, self.settings, self.themes, self.current_theme)
        logger.info("Settings dialog closed.")
        QApplication.processEvents()
        self.isSettingsDialogOpen = False

    @logger.catch
    def closeEvent(self, event):
        logger.info(
            f"Close event triggered with isSettingsDialogOpen={self.isSettingsDialogOpen}"
        )
        if self.isSettingsDialogOpen:
            logger.info("Ignoring close event due to settings dialog being open.")
            event.ignore()
        else:
            logger.info("Proceeding with application quit.")
            app_instance = QApplication.instance()
            if app_instance:
                app_instance.quit()
