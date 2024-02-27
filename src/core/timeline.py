from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
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

        self.video_track_counter = 1
        self.audio_track_counter = 1
        self.tracks = []

        # Button for adding and removing video tracks
        self.add_video_track_button = QPushButton("Add Video Track", self)
        self.add_video_track_button.clicked.connect(
            lambda: self.addTrack(track_type=track_types.video)
        )
        self.layout.addWidget(self.add_video_track_button)

        self.add_audio_track_button = QPushButton("Add Audio Track", self)
        self.add_audio_track_button.clicked.connect(
            lambda: self.addTrack(track_type=track_types.audio)
        )
        self.layout.addWidget(self.add_audio_track_button)

        # Button for adding and removing video tracks
        self.remove_video_track_button = QPushButton("Remove Video Track", self)
        self.remove_video_track_button.clicked.connect(
            lambda: self.removeTrack(track_type=track_types.video)
        )
        self.layout.addWidget(self.remove_video_track_button)

        self.remove_audio_track_button = QPushButton("Remove Audio Track", self)
        self.remove_audio_track_button.clicked.connect(
            lambda: self.removeTrack(track_type=track_types.audio)
        )
        self.layout.addWidget(self.remove_audio_track_button)

        # Initialize with default tracks
        self.addTrack(track_type=track_types.video)
        self.addTrack(track_type=track_types.audio)

    def addTrack(self, track_type):
        name = ""
        if track_type == track_types.video:
            name = f"Video {self.video_track_counter}"
            self.video_track_counter += 1
        elif track_type == track_types.audio:
            name = f"Audio {self.audio_track_counter}"
            self.audio_track_counter += 1
        track = Track(name=name, track_type=track_type, parent=self)
        self.layout.addWidget(track)
        self.tracks.append(track)

    def removeTrack(self, track_type):
        if track_type == track_types.video:
            self.video_track_counter -= 1
        elif track_type == track_types.audio:
            self.audio_track_counter -= 1
        self.layout.removeWidget(self.tracks[-1])
        self.tracks[-1].deleteLater()
        self.tracks.pop()
