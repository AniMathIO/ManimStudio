from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QGraphicsProxyWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen
from PySide6.QtGui import QPainter

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

        # add buttons to the layout
        self.layout.addLayout(self.buttonsLayout)

        self.initializeUI()

    def initializeUI(self):
        # Buttons for adding tracks
        self.add_video_track_button = QPushButton("Add Video Track", self)
        self.add_video_track_button.clicked.connect(
            lambda: self.addTrack(track_types.video)
        )

        self.add_audio_track_button = QPushButton("Add Audio Track", self)
        self.add_audio_track_button.clicked.connect(
            lambda: self.addTrack(track_types.audio)
        )

        # Buttons for removing track
        self.remove_video_track_button = QPushButton("Remove Video Track", self)
        self.remove_video_track_button.clicked.connect(
            lambda: self.removeTrack(track_types.video)
        )

        self.remove_audio_track_button = QPushButton("Remove Audio Track", self)
        self.remove_audio_track_button.clicked.connect(
            lambda: self.removeTrack(track_types.audio)
        )

        # Add buttons to the horizontal layout
        self.buttonsLayout.addWidget(self.add_video_track_button)
        self.buttonsLayout.addWidget(self.add_audio_track_button)
        self.buttonsLayout.addWidget(self.remove_video_track_button)
        self.buttonsLayout.addWidget(self.remove_audio_track_button)

        # Initialize with default tracks
        self.addTrack(track_types.video)
        self.addTrack(track_types.audio)

    def addTrack(self, track_type):
        name = ""
        if track_type == track_types.video:
            name = f"Video {len(self.video_tracks) + 1}"
            track = Track(name=name, track_type=track_type, parent=self)
            self.layout.insertWidget(len(self.video_tracks), track)
            self.video_tracks.append(track)
        elif track_type == track_types.audio:
            name = f"Audio {len(self.audio_tracks) + 1}"
            track = Track(name=name, track_type=track_type, parent=self)
            self.layout.addWidget(track)
            self.audio_tracks.append(track)

    def removeTrack(self, track_type):
        if track_type == track_types.video and len(self.video_tracks) > 1:
            track = self.video_tracks.pop()
            self.layout.removeWidget(track)
            track.deleteLater()
        elif track_type == track_types.audio and len(self.audio_tracks) > 1:
            track = self.audio_tracks.pop()
            self.layout.removeWidget(track)
            track.deleteLater()
