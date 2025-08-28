import math
from enum import Enum

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QInputDialog

from objects_menu.object_manager import ObjectManager


class objs(Enum):
    Vines = 0
    TalkableNPC = 1
    SpawnPoint = 2
    Spike = 3

class ObjectCanvas(QWidget):
    def __init__(self, extent, window_extent):
        super().__init__()
        self.setFixedSize(*window_extent)
        self.manager = ObjectManager()
        self.scale_x = window_extent[0] / extent[0] * 0.5
        self.scale_y = window_extent[1] / extent[1] * 0.5
        self.last_point = None
        self.current_point = None
        self.current_type = "vines"
        self.spike_dir = "Up"

    def add_object(self, start, end):
        if self.current_type == "vines":
            distance = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) / 3
            parts, ok = QInputDialog.getInt(self, "Vines", "Number of parts:", int(distance) + 1, 1, 100)
            if ok:
                self.manager.add_vine(start, end, parts)
        elif self.current_type == "talkable npc":
            dialogue, ok = QInputDialog.getText(self, "NPC", "Dialogue name:")
            if ok:
                self.manager.add_npc(start, end, dialogue)
        elif self.current_type == "spikes":
            self.manager.add_spike(start, end, self.spike_dir)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            current_point = QPoint()
            current_point.setX(int(event.pos().x() / self.scale_x))
            current_point.setY(int(event.pos().y() / self.scale_y))
            if (self.current_type == "spawn point"):
                self.manager.set_spawn_point(current_point)
            self.update()


    def mouseMoveEvent(self, event):
        if (self.last_point != None):
            # Scale the current position to match object coordinates
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
            if (self.current_type == "vines"):
                if self.last_point is not None:
                    (x1, y1), (x2, y2) = self.last_point, (current_point.x(), current_point.y())
                    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) // 2 / 1.5
                    value, ok = QInputDialog.getInt(self, "vines", "input number of vines parts:", int(distance + 1), 1, 100, 1)
                    if ok:
                        self.manager.add_vine((x1, y1), (x2, y2), value)
                        self.last_point = None
                    self.update()
                else:
                    self.last_point = (current_point.x(), current_point.y())
            elif (self.current_type == "talkable npc"):
                if self.last_point is not None:
                    value, ok = QInputDialog.getText(self, "dialogue", "input dialogueName:")
                    if ok:
                        self.manager.add_npc(self.last_point, (current_point.x(), current_point.y()), value)
                        self.last_point = None
                    self.update()
                else:
                    self.last_point = (current_point.x(), current_point.y())
            elif (self.current_type == "spikes"):
                if self.last_point is not None:
                    self.manager.add_spike(self.last_point, (current_point.x(), current_point.y()), self.spike_dir)
                    self.last_point = None
                    self.update()
                else:
                    self.last_point = (current_point.x(), current_point.y())
    def clear(self):
        self.manager.clear()
        self.update()
    def paintEvent(self, event):
        def getPointInScale(point):
            current_point = QPoint()
            current_point.setX(int(point[0] * self.scale_x))
            current_point.setY(int(point[1] * self.scale_y))
            return current_point
        painter = QPainter(self)
        self.manager.draw_all_objects(painter, self.scale_x, self.scale_y)
        pen = QPen(QColor("#FFFFFF"), 1, Qt.SolidLine)
        painter.setPen(pen)
        if self.current_point is not None and self.last_point is not None:
            painter.drawLine(getPointInScale(self.last_point), getPointInScale((self.current_point.x(), self.current_point.y())))


    # just write to file
    def saveObjectsToFile(self, filename):
        self.manager.save_object_to_file(filename)
    def change_object_type(self, type):
        if (type == "vines"):
            self.current_type = "vines"
        elif (type == "player spawn point"):
            self.current_type = "spawn point"
        elif (type == "talkable npc"):
            self.current_type = "talkable npc"
        elif (type == "spikes"):
            self.current_type = "spikes"
        else:
            print("unknown object type")
