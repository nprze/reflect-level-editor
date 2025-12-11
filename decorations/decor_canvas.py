from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget

from game_objects import LineGameObject, PointGameObject
from decorations.decor_manager import decor_manager


class DecorCanvas(QWidget):
    def __init__(self, extent, window_extent):
        super().__init__()
        self.setFixedSize(*window_extent)
        self.scale_x = window_extent[0] / extent[0] * 0.5
        self.scale_y = window_extent[1] / extent[1] * 0.5
        self.last_point = None
        self.current_point = None
        self.current_type = list(decor_manager.get_decor_types())[0]

    def mouseMoveEvent(self, event):
        if (self.last_point != None):
            current_point = QPoint()
            current_point.setX(int(event.pos().x() / self.scale_x))
            current_point.setY(int(event.pos().y() / self.scale_y))
            self.current_point = current_point
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            current_point = QPoint()
            current_point.setX(int(event.pos().x() / self.scale_x))
            current_point.setY(int(event.pos().y() / self.scale_y))
            current_decor_class = decor_manager.decors[self.current_type]["class"]
            current_point = (current_point.x(), current_point.y())
            if (issubclass(current_decor_class, PointGameObject)):
                decor_manager.add_decor(self.current_type, current_point)
            elif (issubclass(current_decor_class, LineGameObject)):
                if (self.last_point != None):
                    decor_manager.add_decor(self.current_type, current_point, self.last_point)
                    self.last_point = None
                else:
                    self.last_point = current_point
            else:
                print(f"unknown type: {self.current_type}!")
            self.update()

    def clear(self):
        decor_manager.clear()
        self.update()
    def paintEvent(self, event):
        def getPointInScale(point):
            current_point = QPoint()
            current_point.setX(int(point[0] * self.scale_x))
            current_point.setY(int(point[1] * self.scale_y))
            return current_point
        painter = QPainter(self)
        decor_manager.draw_all_decors(painter, self.scale_x, self.scale_y)
        pen = QPen(QColor("#FFFFFF"), 1, Qt.SolidLine)
        painter.setPen(pen)
        if self.current_point is not None and self.last_point is not None:
            painter.drawLine(getPointInScale(self.last_point), getPointInScale((self.current_point.x(), self.current_point.y())))


    # just write to file
    def savedecorsToFile(self, filename):
        decor_manager.save_decor_to_file(filename)
    def change_decor_type(self, type):
        if type in decor_manager.get_decor_types():
            self.current_type = type
        else:
            print(f"unknown decor type \"{type}\"")
