from components import Components
from objects_menu.game_objects import *
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPen

class ObjectManager:
    def __init__(self):
        self.vines = []
        self.npcs = []
        self.spikes = []
        self.spawn_point = None

    def add_vine(self, start, end, parts):
        self.vines.append(Vine(start, end, parts))

    def add_npc(self, start, end, dialogue_name):
        self.npcs.append(TalkableNPC(start, end, dialogue_name))

    def add_spike(self, start, end, direction):
        self.spikes.append(Spike(start, end, direction))

    def set_spawn_point(self, point):
        self.spawn_point = point
    def draw_all_objects(self, painter, scale_x, scale_y):

        def getPointInScale(point):
            current_point = QPoint()
            current_point.setX(int(point.x() * scale_x))
            current_point.setY(int(point.y() * scale_y))
            return current_point

        # vines
        pen = QPen(QColor("#B5E61D"), 1, Qt.SolidLine)
        painter.setPen(pen)
        for vine in self.vines:
            vine.draw(painter, scale_x, scale_y)

        # npcs
        pen = QPen(QColor("#0000FF"), 1, Qt.SolidLine)
        painter.setPen(pen)
        for npc in self.npcs:
            npc.draw(painter, scale_x, scale_y)

        # spawn point
        pen = QPen(QColor("#FF0000"), 5, Qt.SolidLine)
        painter.setPen(pen)
        if self.spawn_point is not None:
            painter.drawPoint(getPointInScale(self.spawn_point))

        # spikes
        pen = QPen(QColor("#FF0000"), 1, Qt.SolidLine)
        painter.setPen(pen)
        for spike in self.spikes:
            spike.draw(painter, scale_x, scale_y)

    def clear(self):
        self.vines.clear()
        self.npcs.clear()
        self.spikes.clear()
        self.spawn_point = None

    def save_object_to_file(self, filename):
        with open(filename, "w") as f:
            if (self.spawn_point is not None):
                f.write(f"SpawnPoint: {(round(self.spawn_point.x() / 2, 1), Components.map_size[1] - round(self.spawn_point.y() / 2 - 1, 1))}\n")
            f.write(f"VineCount: {len(self.vines)}\n")
            for i in range(len(self.vines)):
                f.write(f"Vine: {i}" + "\n")
                f.write(f"  start: ({round(self.vines[i].start[0] / 2, 1)}, {Components.map_size[1] - round(self.vines[i].start[1] / 2 - 1, 1)})\n")
                f.write(f"  end: ({round(self.vines[i].end[0] / 2, 1)}, {Components.map_size[1] - round(self.vines[i].end[1] / 2 - 1, 1)})\n")
                f.write(f"  edges: {self.vines[i].parts}" + "\n")
            f.write(f"NPCCount: {len(self.npcs)}\n")
            for i in range(len(self.npcs)):
                f.write(f"NPC: {i}" + "\n")
                f.write(f"  start: ({round(self.npcs[i].start[0] / 2, 1)}, {Components.map_size[1] - round(self.npcs[i].start[1] / 2 - 1, 1)})\n")
                f.write(f"  end: ({round(self.npcs[i].end[0] / 2, 1)}, {Components.map_size[1] - round(self.npcs[i].end[1] / 2 - 1, 1)})\n")
                f.write(f"  interactionRadius: 3" + "\n")
                f.write(f"  dialogueName: {self.npcs[i].dialogue_name}" + "\n")
            f.write(f"SpikeCount: {len(self.spikes)}\n")
            for i in range(len(self.spikes)):
                f.write(f"Spike: {i}" + "\n")
                f.write(f"  start: ({round(self.spikes[i].start[0] / 2, 1)}, {Components.map_size[1] - round(self.spikes[i].start[1] / 2 - 1, 1)})\n")
                f.write(f"  end: ({round(self.spikes[i].end[0] / 2, 1)}, {Components.map_size[1] - round(self.spikes[i].end[1] / 2 - 1, 1)})\n")
                f.write(f"  dir: {self.spikes[i].direction}\n")