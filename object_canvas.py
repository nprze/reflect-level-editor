import math
from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QInputDialog

from components import Components

class objs(Enum):
    Vines = 0


class ObjectCanvas(QWidget):
    def __init__(self, extent, windowExtent):
        super().__init__()

        self.vines = []

        self.setFixedSize(windowExtent[0], windowExtent[1])

        self.scale_x = windowExtent[0] / extent[0] * 0.5
        self.scale_y = windowExtent[1] / extent[1] * 0.5

        self.lastPoint = None
        self.currentlyPoint = None
    def addObject(self, type, obj):
        if (type == objs.Vines):
            (x1, y1), (x2, y2) = obj
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) // 2 / 1.5
            value, ok = QInputDialog.getInt(self, "vines", "input number of vines parts:", int(distance+1),1,100,1)
            if ok:
                obj.append(value)
                self.vines.append(obj)

        else:
            print("unknown object type")

    def mousePressEvent(self, event):
        pass


    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.update()
            self.currentlyPoint = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            current_point = QPoint()
            current_point.setX(int(event.pos().x() / self.scale_x))
            current_point.setY(int(event.pos().y() / self.scale_y))
            if self.lastPoint is not None:
                self.addObject(objs.Vines, [self.lastPoint, (current_point.x(), current_point.y())])
                self.lastPoint = None
                self.update()
            else:
                self.lastPoint = (current_point.x(), current_point.y())
    def clear(self):
        self.vines = []
    def paintEvent(self, event):
        def getPointInScale(point):
            current_point = QPoint()
            current_point.setX(int(point[0] * self.scale_x))
            current_point.setY(int(point[1] * self.scale_y))
            return current_point
        painter = QPainter(self)

        pen = QPen(QColor("#B5E61D"), 1, Qt.SolidLine)
        painter.setPen(pen)
        for line in self.vines:
            painter.drawLine(getPointInScale(line[0]), getPointInScale(line[1]))
        if self.currentlyPoint is not None and self.lastPoint is not None:
            painter.drawLine(getPointInScale(self.lastPoint), self.currentlyPoint)
    def saveObjectsToFile(self, filename):
        with open(filename, "w") as f:
            f.write(f"VineCount: {len(self.vines)}\n")
            for i in range(len(self.vines)):
                f.write(f"Vine: {i}" + "\n")
                f.write(f"  start: ({round(self.vines[i][0][0]/2, 1)}, {Components.map_size[1] - round(self.vines[i][0][1]/2 - 1, 1)} )\n")
                f.write(f"  end: ({round(self.vines[i][1][0]/2, 1)}, {Components.map_size[1] -round(self.vines[i][1][1]/2 - 1, 1) })\n")
                f.write(f"  edges: {self.vines[i][2]}" + "\n")