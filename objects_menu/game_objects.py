from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QInputDialog


class LineGameObject:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    def class_specific_stuff(file):
        pass

    def draw(self, painter, scale_x, scale_y):
        painter.drawLine(self._scale_point(self.start, scale_x, scale_y),
                         self._scale_point(self.end, scale_x, scale_y))

    def save_to_file(self, file, y_minus):
        file.write(f"  start: ({round(self.start[0] / 2, 1)}, {y_minus - round(self.start[1] / 2 - 1, 1)})\n")
        file.write(f"  end: ({round(self.end[0] / 2, 1)}, {y_minus - round(self.end[1] / 2 - 1, 1)})\n")

    @staticmethod
    def _scale_point(point, scale_x, scale_y):
        return QPoint(int(point[0] * scale_x), int(point[1] * scale_y))




class PointGameObject:
    def __init__(self, position):
        self.position = position

    @staticmethod
    def class_specific_stuff(file):
        pass

    def draw(self, painter, scale_x, scale_y):
        painter.drawPoint(self._scale_point(self.position, scale_x, scale_y))

    @staticmethod
    def _scale_point(point, scale_x, scale_y):
        return QPoint(int(point[0] * scale_x), int(point[1] * scale_y))
    def save_to_file(self, file, y_minus):
        file.write(f"  position: ({round(self.position[0] / 2, 1)}, {y_minus - round(self.position[1] / 2 - 1, 1) - 0.5})\n")
