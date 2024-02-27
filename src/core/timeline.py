from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QGraphicsProxyWidget,
    QMenu,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QPainter, QAction

from src.ui.track_ui import Ui_Track


class track_types:
    video = "Video"
    audio = "Audio"


class Track(QWidget):  # Ensure Track inherits from QWidget
    def __init__(self, name, track_type, parent=None):
        super().__init__(parent)  # Call the initializer of the QWidget
        self.ui = Ui_Track()
        self.ui.setupUi(self)  # Pass 'self' as the QWidget instance

        self.name = name
        self.track_type = track_type

        # Set the track label to the name
        self.ui.TrackLabel.setText(self.name)


class Timeline(QWidget):
    layout: QVBoxLayout
    video_track_counter = 1
    audio_track_counter = 1
    scene: QVBoxLayout

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.video_tracks = []
        self.audio_tracks = []

        self.buttonsLayout = QVBoxLayout()

        # Separate layouts for video and audio
        self.videoLayout = QVBoxLayout()
        self.audioLayout = QVBoxLayout()

        self.initializeVideoUI()
        self.initializeAudioUI()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

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

    def initializeVideoUI(self):
        # Initial video track
        self.addTrack(track_types.video)

        # Add the video layout to the main layout
        self.layout.addLayout(self.videoLayout)

    def initializeAudioUI(self):
        # Initial audio track
        self.addTrack(track_types.audio)

        # Add the audio layout to the main layout
        self.layout.addLayout(self.audioLayout)

    def addTrack(self, track_type):
        name = ""
        if track_type == track_types.video:
            name = f"Video {len(self.video_tracks) + 1}"
            track = Track(name=name, track_type=track_type, parent=self)

            self.videoLayout.addWidget(track)
            self.video_tracks.append(track)
        elif track_type == track_types.audio:
            name = f"Audio {len(self.audio_tracks) + 1}"
            track = Track(name=name, track_type=track_type, parent=self)
            self.audioLayout.addWidget(track)
            self.audio_tracks.append(track)

    def removeTrack(self, track_type):
        if track_type == track_types.video and len(self.video_tracks) > 1:
            track = self.video_tracks.pop()
            self.videoLayout.removeWidget(track)
            track.deleteLater()
        elif track_type == track_types.audio and len(self.audio_tracks) > 1:
            track = self.audio_tracks.pop()
            self.audioLayout.removeWidget(track)
            track.deleteLater()