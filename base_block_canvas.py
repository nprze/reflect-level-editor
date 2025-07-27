from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtWidgets import QWidget

from components import Components


# helper functions
def get_non_diagonal(start, end):
    if start.x() == end.x() or start.y() == end.y():
        return [(start, end)]
    x0, y0 = start.x(), start.y()
    x1, y1 = end.x(), end.y()

    points = [(x0, y0)]
    x, y = x0, y0

    dx = 1 if x1 > x0 else -1
    dy = 1 if y1 > y0 else -1

    while (x, y) != (x1, y1):
        if abs(x1 - x) > abs(y1 - y):
            x += dx
        else:
            y += dy
        points.append((x, y))

    segments = []
    prev_x, prev_y = points[0]
    for x, y in points[1:]:
        segments.append((QPoint(prev_x, prev_y), QPoint(x, y)))
        prev_x, prev_y = x, y

    return segments


class BaseBlockCanvas(QWidget):
    def __init__(self, extent, windowExtent):
        super().__init__()


        self.logical_extent = extent
        self.objects = []
        self.lines = []
        self.points = []
        self.drawing = False
        self.last_point = QPoint()

        self.setFixedSize(windowExtent[0], windowExtent[1])

        self.scale_x = windowExtent[0] / self.logical_extent[0]
        self.scale_y = windowExtent[1] / self.logical_extent[1]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            current_point = QPoint()
            current_point.setX(int(event.pos().x()/ self.scale_x))
            current_point.setY(int(event.pos().y()/ self.scale_y))
            self.last_point = current_point

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            current_point = QPoint()
            current_point.setX(int(event.pos().x() / self.scale_x))
            current_point.setY(int(event.pos().y() / self.scale_y))

            if current_point != self.last_point:
                for line in get_non_diagonal(self.last_point, current_point):
                    self.lines.append((Components.brush_color, line[0], line[1]))
                self.last_point = current_point
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            current_point = QPoint()
            current_point.setX(int(event.pos().x() / self.scale_x))
            current_point.setY(int(event.pos().y() / self.scale_y))

            if current_point == self.last_point:
                self.points.append((Components.brush_color, current_point))
                self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#000000"))

        # draw helper lines
        pen = QPen(QColor("#0F0F0F"), 1, Qt.SolidLine)
        painter.setPen(pen)
        for i in range(self.logical_extent[0]-1):
            painter.drawLine(QPoint(int((i+1) * self.scale_x), 0), QPoint(int((i+1) * self.scale_x), Components.editor_map_size[1]))
        for i in range(self.logical_extent[1]-1):
            painter.drawLine(QPoint(0, int((i+1) * self.scale_y)), QPoint(Components.editor_map_size[0], int((i+1) * self.scale_y)))

        painter.scale(self.scale_x, self.scale_y)
        pen.setCosmetic(True)
        for line in self.lines:
            pen = QPen(line[0], 1, Qt.SolidLine)
            painter.setPen(pen)
            adjusted_p1 = QPointF(line[1].x() + 0.5, line[1].y() + 0.5)
            adjusted_p2 = QPointF(line[2].x() + 0.5, line[2].y() + 0.5)
            painter.drawLine(adjusted_p1, adjusted_p2)
        for point in self.points:
            pen = QPen(point[0], 1, Qt.SolidLine)
            painter.setPen(pen)
            adjusted_point = QPointF(point[1].x() + 0.5, point[1].y() + 0.5)
            painter.drawPoint(adjusted_point)
