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
)
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QPainter, QAction, QColor
from PySide6.QtSvgWidgets import QSvgWidget
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
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)


class Timeline(QWidget):
    layout: QVBoxLayout
    video_track_counter = 1
    audio_track_counter = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
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

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setFrameShape(QFrame.Shape.NoFrame)
        self.view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.view.setStyleSheet("background: transparent; border: none")

        # Make the QGraphicsView overlay the existing layout
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.view)
        self.layout.addWidget(self.stack)

        self.view.setSceneRect(QRectF(0, 0, self.view.width(), self.view.height()))

        # Default timeline length in seconds (5 minutes)
        self.defaultTimelineLength = 5 * 60
        # Draw the indicator line
        self.indicatorLine = QGraphicsLineItem(0, 0, 0, 1000)  # Temporary height
        self.indicatorLine.setPen(QPen(QColor(255, 0, 0), 2))  # Red line
        self.indicatorLine.setZValue(
            1
        )  # Ensure it's above other items which have a default Z-value of 0

        self.scene.addItem(self.indicatorLine)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update the scene rect to match the new size
        self.view.setSceneRect(0, 0, self.width(), self.height())
        # Adjust the indicator height to match the Timeline height
        if self.indicatorLine:
            line = self.indicatorLine.line()
            self.indicatorLine.setLine(line.x1(), line.y1(), line.x2(), self.height())

    def updateIndicatorLineHeight(self):
        # Assuming self.height() gives the desired height of the indicator
        self.indicatorLine.setLine(0, 0, 0, self.height())

    def updateIndicatorPosition(self, sliderValue, sliderMaximum):
        # Map sliderValue to x-coordinate in the scene
        xPos = self.mapSliderValueToXPosition(sliderValue, sliderMaximum)
        self.indicatorLine.setPos(xPos, 0)

    def mapSliderValueToXPosition(self, sliderValue, sliderMaximum):
        # Use the width of the QGraphicsView as the scaling reference
        timelineWidth = self.view.width()

        # Calculate the proportion of the slider value to its maximum
        proportion = sliderValue / sliderMaximum

        # Apply this proportion to the timeline's width to get the x-position
        xPos = proportion * timelineWidth

        return xPos

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

    def removeTrack(self, track_type):
        if track_type == track_types.video and len(self.video_tracks) > 1:
            track = self.video_tracks.pop()
            self.videoLayout.removeWidget(track)
            track.deleteLater()
        elif track_type == track_types.audio and len(self.audio_tracks) > 1:
            track = self.audio_tracks.pop()
            self.audioLayout.removeWidget(track)
            track.deleteLater()
