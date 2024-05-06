from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QGraphicsProxyWidget,
    QSizePolicy,
    QMenu,
    QStackedWidget,
    QGraphicsLineItem,
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsItem,
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QPainter, QAction, QColor, QPixmap, QImage
from PySide6.QtSvgWidgets import QSvgWidget
from src.ui.track_ui import Ui_Track
from src.utils.logger_utility import logger
import os
from pydub import AudioSegment
import numpy as np


class track_types:
    video = "Video"
    audio = "Audio"


class Track(QWidget):  # Ensure Track inherits from QWidget
    @logger.catch
    def __init__(self, name, track_type, parent=None):
        super().__init__(parent)  # Call the initializer of the QWidget
        self.ui = Ui_Track()
        self.ui.setupUi(self)  # Pass 'self' as the QWidget instance

        self.name = name
        self.track_type = track_type

        # Set the track label to the name
        self.ui.TrackLabel.setText(self.name)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setAcceptDrops(True)

        self.graphicsView = self.ui.trackGraphicsView
        self.graphicsScene = QGraphicsScene(self)
        self.graphicsView.setScene(self.graphicsScene)

    @logger.catch
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
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
                pixmap = QPixmap(file_path)
                pixmap_item = QGraphicsPixmapItem(pixmap)
                drop_position = self.graphicsView.mapFromScene(event.pos())
                pixmap_item.setPos(drop_position)
                self.graphicsScene.addItem(pixmap_item)
        else:
            event.ignore()


class ResizableRectItem(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.resizing = False

    def hoverMoveEvent(self, event):
        if self.isSelected() and event.pos().x() > self.rect().right() - 10:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if event.pos().x() > self.rect().right() - 10:
            self.resizing = True
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.resizing:
            new_width = event.pos().x() - self.rect().left()
            self.setRect(
                QRectF(
                    self.rect().left(),
                    self.rect().top(),
                    new_width,
                    self.rect().height(),
                )
            )
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            new_pos = value
            scene_rect = self.scene().sceneRect()
            if not scene_rect.contains(new_pos):
                new_pos.setX(max(new_pos.x(), scene_rect.left()))
                new_pos.setX(min(new_pos.x(), scene_rect.right() - self.rect().width()))
                new_pos.setY(max(new_pos.y(), scene_rect.top()))
                new_pos.setY(
                    min(new_pos.y(), scene_rect.bottom() - self.rect().height())
                )
                return new_pos
        return super().itemChange(change, value)


class Timeline(QWidget):
    layout: QVBoxLayout
    video_track_counter = 1
    audio_track_counter = 1
    indicatorLine: QGraphicsLineItem

    @logger.catch
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        self.sliderValue = 0
        self.sliderMaximum = 1
        self.setAcceptDrops(True)

    @logger.catch
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    @logger.catch
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.handle_dropped_file(file_path, event.pos())
        else:
            event.ignore()

    @logger.catch
    def handle_dropped_file(self, file_path, scene_position):
        pixmap = QPixmap(file_path)
        pixmap_item = QGraphicsPixmapItem(pixmap)
        drop_position = self.view.mapFromScene(scene_position)
        track = self.find_track_at_position(drop_position)
        if track:
            track.graphicsScene.addItem(pixmap_item)
            pixmap_item.setPos(track.graphicsView.mapFromScene(drop_position))

    def addMediaToTimeline(self, file_path):
        logger.info(f"Adding media to timeline: {file_path}")

        track = self.find_available_track(file_path)
        logger.info(f"Found track: {track}")
        if track:
            if file_path.lower().endswith((".mp3", ".wav", ".flac")):  # Audio file
                audio = AudioSegment.from_file(file_path)
                samples = audio.get_array_of_samples()
                samples = np.array(samples)
                samples = samples.reshape((-1, audio.channels))
                waveform_data = np.mean(samples, axis=1)

                # Normalize waveform data
                max_amplitude = np.max(np.abs(waveform_data))
                normalized_data = waveform_data / max_amplitude

                # Create QImage for the waveform
                width = 100
                height = track.graphicsView.height() - 10
                image = QImage(width, height, QImage.Format.Format_ARGB32)
                image.fill(Qt.GlobalColor.transparent)

                painter = QPainter(image)
                painter.setPen(Qt.GlobalColor.black)
                for x in range(width):
                    sample_index = int((x / width) * len(normalized_data))
                    sample = normalized_data[sample_index]
                    painter.drawLine(
                        x, (1 - sample) * height / 2, x, (1 + sample) * height / 2
                    )
                painter.end()

                pixmap = QPixmap.fromImage(image)
            else:  # Image or video file
                pixmap = QPixmap(file_path)
                if pixmap.isNull():
                    logger.warning(f"Failed to load pixmap from file: {file_path}")
                    return

            # Create a ResizableRectItem with the desired size
            rect_item = ResizableRectItem(0, 0, 100, track.graphicsView.height() - 10)

            # Set the brush and pen for the rectangle
            rect_item.setBrush(Qt.BrushStyle.NoBrush)
            pen = QPen(Qt.GlobalColor.black, 2)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            rect_item.setPen(pen)

            # Create a QGraphicsPixmapItem with the preview image or waveform
            pixmap_item = QGraphicsPixmapItem(
                pixmap.scaled(
                    rect_item.boundingRect().size().toSize(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
            pixmap_item.setParentItem(rect_item)
            pixmap_item.setPos(
                (rect_item.boundingRect().width() - pixmap_item.boundingRect().width())
                / 2,
                (
                    rect_item.boundingRect().height()
                    - pixmap_item.boundingRect().height()
                )
                / 2,
            )

            # Align the rect_item to the left of the track
            scene_rect = track.graphicsScene.sceneRect()
            if not track.graphicsScene.items():
                rect_item.setPos(scene_rect.left(), rect_item.pos().y())
            else:
                last_item = track.graphicsScene.items()[-1]
                rect_item.setPos(
                    last_item.pos().x() + last_item.rect().width(), rect_item.pos().y()
                )

            track.graphicsScene.addItem(rect_item)

    def find_available_track(self, file_path):
        # Determine the track type based on the file extension or other criteria
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()

        if file_extension in [
            ".png",
            ".jpg",
            ".mp4",
            ".mov",
            ".avi",
            ".mkv",
        ]:  # Video files
            if self.video_tracks:
                return self.video_tracks[0]  # Add to the first video track
        elif file_extension in [".mp3", ".wav", ".flac"]:  # Audio files
            if self.audio_tracks:
                return self.audio_tracks[0]  # Add to the first audio track

        return None

    @logger.catch
    def find_track_at_position(self, position):
        for track in self.video_tracks + self.audio_tracks:
            if track.graphicsView.geometry().contains(position):
                return track
        return None

    @logger.catch
    def setupUI(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setLayout(self.layout)

        self.video_tracks = []
        self.audio_tracks = []

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.configureIndicatorGraphicsView()

        self.indicatorLine = QGraphicsLineItem(0, 0, 0, 100)
        self.indicatorLine.setPen(QPen(QColor(255, 0, 0), 2))
        self.indicatorLine.setZValue(1)
        self.scene.addItem(self.indicatorLine)

        # Initialize layouts for tracks
        self.initializeTracksUI()

        self.view.raise_()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    @logger.catch
    def configureIndicatorGraphicsView(self):
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setFrameShape(QFrame.Shape.NoFrame)
        self.view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.view.setStyleSheet("background: transparent;")
        self.view.setGeometry(0, 0, self.width(), self.height())

    @logger.catch
    def updateIndicatorLineHeight(self):
        # Calculate the new height based on the tracks
        trackHeight = self.calculateTracksHeight()
        nameSeparatorEndX = self.calculateNameSeparatorEndX()
        if self.indicatorLine:
            # Set the new line starting after the track labels
            self.indicatorLine.setLine(
                nameSeparatorEndX, 0, nameSeparatorEndX, trackHeight
            )

    @logger.catch
    def updateIndicatorView(self):
        self.view.setGeometry(0, 0, self.width(), self.height())
        self.view.raise_()
        self.updateIndicatorLineHeight()

    @logger.catch
    def calculateTracksHeight(self):
        # Calculate combined height based on track count
        return 230 * (len(self.video_tracks) + len(self.audio_tracks))

    @logger.catch
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view.setGeometry(0, 0, self.width(), self.height())
        self.view.setSceneRect(QRectF(0, 0, self.width(), self.height()))
        self.updateIndicatorView()
        self.updateIndicatorPosition(self.sliderValue, self.sliderMaximum)

    @logger.catch
    def updateIndicatorPosition(self, sliderValue, sliderMaximum):
        self.sliderValue = sliderValue
        self.sliderMaximum = sliderMaximum
        proportion = sliderValue / sliderMaximum
        xPos = proportion * (self.width() - self.indicatorLine.line().p2().x())
        self.indicatorLine.setPos(xPos, 0)

    @logger.catch
    def initializeTracksUI(self):
        self.videoLayout = QVBoxLayout()
        self.audioLayout = QVBoxLayout()
        self.initializeVideoUI()
        self.initializeAudioUI()

    @logger.catch
    def calculateNameSeparatorEndX(self):
        # Implement the actual calculation of the NameSeparator's end position here
        # For example, you might iterate over all tracks and find the maximum end position
        maxSeparatorEndX = 0
        for track in self.video_tracks + self.audio_tracks:
            separatorEndX = (
                track.ui.NameSeparator.geometry().right()
            )  # Assuming NameSeparator is the object name
            maxSeparatorEndX = max(maxSeparatorEndX, separatorEndX)
        return maxSeparatorEndX

    @logger.catch
    def showContextMenu(self, position):
        current_background_color = self.palette().color(self.backgroundRole())

        darker_color = current_background_color.darker(120)

        self.setStyleSheet(
            f"""
        QMenu::item:selected {{
        background-color: {darker_color.name()};
        }}
        """
        )

        contextMenu = QMenu(self)
        addVideoTrackAction = contextMenu.addAction("Add Video Track")
        addVideoTrackAction.triggered.connect(lambda: self.addTrack(track_types.video))

        addAudioTrackAction = contextMenu.addAction("Add Audio Track")
        addAudioTrackAction.triggered.connect(lambda: self.addTrack(track_types.audio))

        addVideoTrackAction = contextMenu.addAction("Remove Video Track")
        addVideoTrackAction.triggered.connect(
            lambda: self.removeTrack(track_types.video)
        )

        addAudioTrackAction = contextMenu.addAction("Remove Audio Track")
        addAudioTrackAction.triggered.connect(
            lambda: self.removeTrack(track_types.audio)
        )

        contextMenu.exec(self.mapToGlobal(position))

    @logger.catch
    def initializeVideoUI(self):
        # Initial video track
        self.addTrack(track_types.video)

        # Add the video layout to the main layout
        self.layout.addLayout(self.videoLayout)

    @logger.catch
    def initializeAudioUI(self):
        # Initial audio track
        self.addTrack(track_types.audio)

        # Add the audio layout to the main layout
        self.layout.addLayout(self.audioLayout)

    @logger.catch
    def addTrack(self, track_type):
        name = ""
        if track_type == track_types.video:
            name = f"Video {len(self.video_tracks) + 1}"
            track = Track(name=name, track_type=track_type, parent=self)
            track.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            self.videoLayout.addWidget(track)
            self.video_tracks.append(track)
        elif track_type == track_types.audio:
            name = f"Audio {len(self.audio_tracks) + 1}"
            track = Track(name=name, track_type=track_type, parent=self)

            track.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
            )
            self.audioLayout.addWidget(track)
            self.audio_tracks.append(track)
        self.updateIndicatorView()

    @logger.catch
    def removeTrack(self, track_type):
        if track_type == track_types.video and len(self.video_tracks) > 1:
            track = self.video_tracks.pop()
            self.videoLayout.removeWidget(track)
            track.deleteLater()
        elif track_type == track_types.audio and len(self.audio_tracks) > 1:
            track = self.audio_tracks.pop()
            self.audioLayout.removeWidget(track)
            track.deleteLater()
        self.updateIndicatorView()
