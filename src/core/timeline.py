from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QStyleOptionGraphicsItem,
    QGraphicsSceneMouseEvent,
    QPushButton,
    QGraphicsRectItem,
    QGraphicsSceneHoverEvent,
    QGraphicsTextItem,
)
from PySide6.QtGui import (
    QMouseEvent,
    QKeyEvent,
    QPen,
    QBrush,
    QColor,
    QPainter,
    QFont,
    QFontMetrics,
    QPolygonF,
)
from PySide6.QtCore import (
    QPoint,
    QPointF,
    QRect,
    QRectF,
    Qt,
    QEvent,
    QLine,
    QSizeF,
)

# Utils imports
from src.utils.logger_utility import logger

# UI imports
from src.ui.track_ui import Ui_TrackContainer


class GraphicsScene(QGraphicsScene):
    @logger.catch
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

    @logger.catch
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.sendSceneMouseEventSignal(event)
        self.mousePressEvent(event)

    @logger.catch
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self.sendSceneMouseEventSignal(event)
        self.mouseReleaseEvent(event)

    @logger.catch
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        self.sendSceneMouseEventSignal(event)
        self.mouseMoveEvent(event)

    @logger.catch
    def sendSceneMouseEventSignal(self, event: QGraphicsSceneMouseEvent):
        self.sendSceneMouseEventSignal(event)


class GraphicsView(QGraphicsView):
    @logger.catch
    def __init__(self, scene: QGraphicsScene):
        super().__init__(scene)

    @logger.catch
    def mousePressEvent(self, event: QMouseEvent):
        self.mousePressEvent(event)

    @logger.catch
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.mouseReleaseEvent(event)

    @logger.catch
    def mouseMoveEvent(self, event: QMouseEvent):
        self.mouseMoveEvent(event)

    @logger.catch
    def sendMousePressEventSignal(self, event: QMouseEvent):
        self.mousePressEvent(event)

    @logger.catch
    def sendMouseReleaseEventSignal(self, event: QMouseEvent):
        self.mouseReleaseEvent(event)

    @logger.catch
    def sendMouseMoveEventSignal(self, event: QMouseEvent):
        self.mouseMoveEvent(event)

    @logger.catch
    def keyPressEvent(self, event: QKeyEvent):
        logger.info("Key pressed")
        self.keyPressEvent(event)

    @logger.catch
    def drawBackground(self, painter: QPainter, rect: QRectF):
        brush: QBrush = QBrush(QColor("#444"))
        painter.fillRect(rect, brush)


class Indicator(QGraphicsItem):
    points = []
    brush: QBrush
    pen: QPen
    line: QLine
    poly: QPolygonF
    pressed: bool = False
    height: float

    @logger.catch
    def __init__(self, height: float):
        super().__init__()
        self.height = height

        self.pen = QPen(Qt.GlobalColor.black, 2)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.brush = QBrush(QColor("#fff"))

        self.points.append(QPointF(-10, 0))
        self.points.append(QPointF(10, 20))
        self.points.append(QPointF(10, -10))
        self.points.append(QPointF(-10, -10))

        self.line = QLine(QPoint(0, 0), QPoint(0, int(self.height)))

        self.setHeight(5, 30)
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    @logger.catch
    def calculateSize(self):
        min_x: float = self.points[0].x()
        min_y: float = self.points[0].y()
        max_x: float = self.points[0].x()
        max_y: float = self.points[0].y()

        for point in self.points:
            if point.x() < min_x:
                min_x = point.x()

            if point.y() < min_y:
                min_y = point.y()

            if point.x() > max_x:
                max_x = point.x()

            if point.y() > max_y:
                max_y = point.y()

        return QSizeF(max_x - min_x, self.line.p2().y())

    @logger.catch
    def setHeight(self, num_tracks: int, track_height: float):
        total_height = num_tracks * track_height
        self.line.setP2(QPoint(0, int(total_height) + 10))
        self.update()

    @logger.catch
    def boundingRect(self):
        size: QSizeF = self.calculateSize()
        return QRectF(-10, -10, size.width(), size.height())

    @logger.catch
    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        painter.setPen(self.pen)
        painter.drawLine(self.line)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.points)

    @logger.catch
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.type() == QEvent.Type.MouseButtonPress:
            self.pressed = True
            logger.info("Mouse pressed")
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self.pressed = False
            logger.info("Mouse released")

        QGraphicsItem.mousePressEvent(self, event)
        self.update()

    @logger.catch
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        pos: QPointF = event.scenePos()
        logger.info(f"Mouse moved to: {pos}")

        if self.pressed:
            self.setPos(pos)

        QGraphicsItem.mouseMoveEvent(self, event)
        self.update()

    @logger.catch
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self.pressed = False
        logger.info("Mouse released")
        QGraphicsItem.mouseReleaseEvent(self, event)
        self.update()

    @logger.catch
    def hoverEnterEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse entered")

    @logger.catch
    def hoverMoveEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse moved")

        # if self.pressed:
        #     pos: QPointF = event.scenePos()
        #     logger.info(f"Mouse moved to: {pos}")
        #     self.setPos(pos)

    @logger.catch
    def hoverLeaveEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse left")
        # self.pressed = False

    @logger.catch
    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if (
            change == QGraphicsItem.GraphicsItemChange.ItemPositionChange
            and self.scene()
        ):
            new_pos = value
            new_pos.setY(self.y())
            if new_pos.x() < 0:
                new_pos.setX(0)

            return new_pos

        return QGraphicsItem.itemChange(self, change, value)


class Track(QGraphicsRectItem):
    color: QColor
    outlineColor: QColor
    selectedColor: QColor
    selectedOutlineColor: QColor
    penWidth: int
    rounded: int
    hasShadow: bool
    thresholdShadow: float
    brush: QBrush
    pen: QPen
    length: int
    height: int
    pressed: bool = False
    oldPos: QPointF
    oldMousePos: QPointF

    @logger.catch
    def __init__(
        self,
        length=100,
        height=30,
        color=QColor("cyan"),
        parent=None,
    ):
        super().__init__(0, 0, length, height)
        self.setAcceptHoverEvents(True)
        self.addButton = QPushButton("Add")
        self.addButton.hide()

        self.length = length
        self.height = height
        self.pen = QPen()
        self.brush = QBrush()
        # self.pen.setColor(QColor("black"))
        # self.pen.setWidth(2)
        # self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        # self.pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

    @logger.catch
    def boundingRect(self):
        return QRect(0, 0, self.length, self.height)

    @logger.catch
    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)

        font = painter.font()
        fontMetrics = QFontMetrics(font)
        text = "tReplaySong1"
        heightFont = fontMetrics.boundingRect(text).height()
        painter.drawRect(self.boundingRect())

    @logger.catch
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse pressed")
        self.pressed = True
        self.oldMousePos = event.scenePos()
        self.oldPos = self.scenePos()

    @logger.catch
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse moved")

        if self.pressed:
            newPos = event.scenePos()
            logger.info(f"New pos: {newPos}")
            yDiff = newPos.y() - self.oldPos.y()
            logger.info(f"Y diff: {abs(yDiff)}")
            heightDiff = 15

            if abs(yDiff) > heightDiff:
                heightDiff *= 2
                heightDiff += 5
                d = int(yDiff % heightDiff)  # noqa: F841
                newPos.setY(self.oldPos.y() + int(yDiff / heightDiff) * heightDiff)
                self.setY(newPos.y())
            else:
                self.setY(self.oldPos.y())

            dx: float = (newPos - self.oldMousePos).x()
            self.setX(self.oldPos.x() + dx)

    @logger.catch
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse released")
        self.pressed = False
        self.oldMousePos = event.scenePos()
        self.oldPos = self.scenePos()

    @logger.catch
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse double clicked")

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        self.addButton.show()
        logger.info("Mouse entered")

    def hovreLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        self.addButton.hide()
        logger.info("Mouse left")


class TrackContainer(QGraphicsRectItem):
    def __init__(self, title, y_position):
        super().__init__(0, y_position, 800, 100)
        self.setBrush(QBrush(QColor(200, 200, 200, 100)))
        self.title = title

        titleItem = QGraphicsTextItem(title, self)
        titleItem.setPos(5, -20)

        self.titleItem = titleItem

        self.addButton = QGraphicsRectItem(750, 35, 40, 30, self)
        self.addButton.setBrush(QBrush(Qt.GlobalColor.green))
        self.addButton.setToolTip("Click to add a new track")

    def mousePressEvent(self, event):
        if self.addButton.contains(event.pos()):
            logger.info(f"Adding new track to {self.title()}")
            self.addNewTrack()

    def addNewTrack(self):
        logger.info(f"Adding new track to {self.titleItem.toPlainText()}")


class CustomGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initTrackContainers()

    def initTrackContainers(self):
        self.videoTrackContainer = TrackContainer("Video Tracks", 50)
        self.addItem(self.videoTrackContainer)

        self.audioTrackContainer = TrackContainer(
            "Audio Tracks", 200
        )  # Adjust spacing as needed
        self.addItem(self.audioTrackContainer)

    def addTrack(self, type, length):
        # Placeholder for track adding logic
        print(f"Adding {type} track of length {length}")


class Timeline(QWidget):
    frame: int
    min_frame: int
    max_frame: int
    scene: QGraphicsScene
    view: QGraphicsView

    @logger.catch
    def __init__(self, view: QGraphicsView, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.view = view
        if not self.view.scene():
            self.view.setScene(
                QGraphicsScene(self.view)
            )  # Initialize the scene if it's not already set
        self.scene = self.view.scene()
        self.setMouseTracking(True)
        self.setupScene()

        # set a minimum and maximum width and height for the scene
        min_width: int = 0
        min_height: int = 0
        max_width: int = 1000
        max_height: int = 1000
        self.scene.setSceneRect(min_width, min_height, max_width, max_height)

        # timeline segmentation
        x_offset: int = 100
        for i in range(10):
            item: QGraphicsItem = self.scene.addText(f"{i}")
            item.setPos(i * x_offset, min_height)

        # current frame indicator
        indicator = Indicator(self.height() + 30)
        self.scene.addItem(indicator)
        indicator.setZValue(101)

        # add separator lines between tracks - horizontal lines
        self.drawSeparators(self.scene)

        # add tracks
        track = Track()
        self.scene.addItem(track)
        track.setPos(0, 30)

    def setupScene(self):
        if not self.view.scene():
            self.view.setScene(QGraphicsScene(self))
        self.scene = self.view.scene()
        self.scene.setSceneRect(0, 0, 1000, 600)  # Example dimensions

        self.initTrackContainers()
        self.initTimelineSegments()
        self.initCurrentFrameIndicator()

    def initTrackContainers(self):
        # Setup track containers for video and audio within the scene
        self.videoTrackContainer = TrackContainer("Video Tracks", 50)
        self.scene.addItem(self.videoTrackContainer)

        self.audioTrackContainer = TrackContainer("Audio Tracks", 200)
        self.scene.addItem(self.audioTrackContainer)

    def initTimelineSegments(self):
        x_offset = 100
        for i in range(10):
            item = self.scene.addText(f"{i}")
            item.setPos(i * x_offset, 0)

    def initCurrentFrameIndicator(self):
        indicator = Indicator(600)  # Pass the height as needed
        self.scene.addItem(indicator)
        indicator.setZValue(101)

    @logger.catch
    def addItem(self, pos: QPointF, rect: QRect, pen: QPen, brush: QBrush):
        item: QGraphicsItem = self.scene.addRect(rect, pen, brush)
        item.setPos(pos)

    def drawSeparators(self, scene: QGraphicsScene):
        painter = QPainter(self.view.viewport())
        pen = QPen()
        pen.setColor(Qt.GlobalColor.red)
        painter.setPen(pen)

        track_height = 30  # Height of each track, adjust as necessary
        num_tracks = 2  # Number of tracks, adjust as necessary

        for i in range(1, num_tracks):
            y = i * track_height
            painter.drawLine(0, y, self.width(), y)

    def initSeparators(self):
        track_height = 100  # Adjust based on your layout
        num_tracks = 2  # For video and audio
        pen = QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine)
        for i in range(1, num_tracks):
            y = i * track_height
            line = self.scene.addLine(0, y, self.scene.width(), y, pen)
            line.setZValue(100)  # Ensure it's drawn above other items
