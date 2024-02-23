from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QStyleOptionGraphicsItem,
    QGraphicsSceneMouseEvent,
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


class Track(QGraphicsItem):
    color: QColor
    outline_color: QColor
    selected_color: QColor
    selected_outline_color: QColor
    pen_width: int
    rounded: int
    has_shadow: bool
    threshold_shadow: float
    brush: QBrush
    pen: QPen
    length: int
    height: int
    pressed: bool = False
    old_pos: QPointF
    old_mouse_pos: QPointF
    my_scene: Optional[QGraphicsScene] = None

    @logger.catch
    def __init__(
        self,
        my_scene: Optional[QGraphicsScene] = None,
        length=5,
        color=QColor("black"),
        parent=None,
    ):
        super().__init__(parent)
        self.rounded = 5
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.color = color
        self.outline_color = self.color.lighter(130)

        # self.selected_color = QColor(255, 30, 180)
        # self.selected_color_outline = self.selected_color.lighter(130)
        # self.rounded = 3
        # self.hasShadow = True
        # self.treshold_shadow = 0.0

        self.brush = QBrush(self.color)
        self.pen_width = 2
        self.pen = QPen(self.outline_color, self.pen_width)
        self.pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.length = length
        self.height = 30
        self.old_pos = self.scenePos()
        self.my_scene = my_scene

    @logger.catch
    def boundingRect(self):
        return QRect(0, 0, self.length, self.height)

    @logger.catch
    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawRoundedRect(self.boundingRect(), self.rounded, self.rounded)
        painter.setBrush(self.outline_color)
        font: QFont = self.scene().font()
        font_metrics: QFontMetrics = QFontMetrics(font)
        text: str = "tReplaySong1"
        height_font: int = font_metrics.boundingRect(text).height()
        painter.drawText(0, height_font, text)

    @logger.catch
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse pressed")
        self.pressed = True
        self.old_mouse_pos = event.scenePos()
        self.old_pos = self.scenePos()

    @logger.catch
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse moved")

        if self.pressed:
            new_mouse_pos: QPointF = event.scenePos()
            logger.info(f"New pos: {new_mouse_pos}")
            y_diff: float = new_mouse_pos.y() - self.old_mouse_pos.y()
            logger.info(f"Y diff: {abs(y_diff)}")
            height_diff: int = 15

            if abs(y_diff) > height_diff:
                height_diff *= 2
                height_diff += 5
                d: int = int(y_diff % height_diff)  # noqa: F841
                new_mouse_pos.setY(
                    self.old_mouse_pos.y() + int(y_diff / height_diff) * height_diff
                )
                self.setY(new_mouse_pos.y())
            else:
                self.setY(self.old_mouse_pos.y())

            dx: float = (new_mouse_pos - self.old_mouse_pos).x()
            self.setX(self.old_pos.x() + dx)

    @logger.catch
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse released")
        self.pressed = False

        # if the track's position is out of bounds, reset it to the old position
        # TODO: change this so it's not out of bound from parent scene
        if self.x() < 0:
            self.setX(0)
        if self.y() < 0:
            self.setY(30)
        if self.x() + self.length > self.scene().width():
            self.setX(self.scene().width() - self.length)
        if self.y() + self.height > self.scene().height():
            self.setY(self.scene().height() - self.height)

        self.old_mouse_pos = event.scenePos()
        self.old_pos = self.scenePos()

    @logger.catch
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        logger.info("Mouse double clicked")


class TrackContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TrackContainer()
        self.ui.setupUi(self)

    def setTrackName(self, name: str):
        self.ui.TrackName.setText(name)

    def setTrackColor(self, color: QColor):
        self.ui.TrackFrame.setStyleSheet(f"background-color: {color.name()};")


class Timeline(QWidget):
    frame: int
    min_frame: int
    max_frame: int
    scene: QGraphicsScene
    view: QGraphicsView

    @logger.catch
    def __init__(self, _view: QGraphicsView, _parent=None):
        super().__init__(_parent)
        self.view = _view
        if not self.view.scene():
            self.view.setScene(
                QGraphicsScene(self.view)
            )  # Initialize the scene if it's not already set
        self.scene = self.view.scene()
        self.setMouseTracking(True)

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
        track: Track = Track(self.scene, 200, QColor("black"))
        self.scene.addItem(track)
        track.setPos(QPointF(min_width, min_height + 30))

    @logger.catch
    def addItem(self, pos: QPointF, rect: QRect, pen: QPen, brush: QBrush):
        item: QGraphicsItem = self.scene.addRect(rect, pen, brush)
        item.setPos(pos)

    def drawSeparators(self, scene: QGraphicsScene):
        painter = QPainter(self.view.viewport())
        pen = QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        track_height = 30  # Height of each track, adjust as necessary
        num_tracks = 2  # Number of tracks, adjust as necessary

        for i in range(1, num_tracks):
            y = i * track_height
            painter.drawLine(0, y, self.width(), y)
