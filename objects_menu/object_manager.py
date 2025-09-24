from components import Components
from objects_menu.game_objects import *


'''
class ObjectManager:
    def __init__(self):
        self.vines = []
        self.npcs = []
        self.spikes = []
        self.basic_enemies = []
        self.jump_boosters = []
        self.dash_recharge = []
        self.spawn_point = None

    def add_vine(self, start, end, parts):
        self.vines.append(Vine(start, end, parts))

    def add_npc(self, start, end, dialogue_name):
        self.npcs.append(TalkableNPC(start, end, dialogue_name))

    def add_spike(self, start, end, direction):
        self.spikes.append(Spike(start, end, direction))

    def add_base_enemy(self, position, animation_name):
        self.basic_enemies.append(BasicEnemy(position, [-1, -1], [1, 1], animation_name))

    def add_jump_boost(self, position):
        self.jump_boosters.append(JumpBooster(position, [-1, 0], [1, 1]))

    def add_dash_recharge(self, position):
        self.dash_recharge.append(DashRecharge(position))

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

        # basic enemies
        pen = QPen(QColor("#FF00FF"), 1, Qt.SolidLine)
        painter.setPen(pen)
        for enemy in self.basic_enemies:
            enemy.draw(painter, scale_x, scale_y)

        # jump boosters
        pen = QPen(QColor("#FFFF00"), 1, Qt.SolidLine)
        painter.setPen(pen)
        for boost in self.jump_boosters:
            boost.draw(painter, scale_x, scale_y)

        # jump boosters
        pen = QPen(QColor("#0066FF"), 5, Qt.SolidLine)
        painter.setPen(pen)
        for dash in self.dash_recharge:
            dash.draw(painter, scale_x, scale_y)

    def clear(self):
        self.vines.clear()
        self.npcs.clear()
        self.spikes.clear()
        self.basic_enemies.clear()
        self.jump_boosters.clear()
        self.dash_recharge.clear()
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
                f.write(f"BasicEnemyCount: {len(self.basic_enemies)}" + "\n")
                for i in range(len(self.basic_enemies)):
                    f.write(f"BasicEnemy: {i}" + "\n")
                    f.write(f"  position: ({round(self.basic_enemies[i].position[0] / 2, 1)}, {Components.map_size[1] - round(self.basic_enemies[i].position[1] / 2 - 1, 1)})\n")
                    f.write(f"  min: ({round(self.basic_enemies[i].min[0] / 2, 1)}, {round(self.basic_enemies[i].min[1] / 2, 1)})\n")
                    f.write(f"  max: ({round(self.basic_enemies[i].max[0] / 2, 1)}, {round(self.basic_enemies[i].max[1] / 2, 1)})\n")
                    f.write(f"  animName: {self.basic_enemies[i].animation_name}\n")
                f.write(f"JumpBoosterCount: {len(self.jump_boosters)}\n")
                if (len(self.jump_boosters) != 0):
                    f.write(f"JumpBoosterFile: anim/jump_boost/basic-enemy-walk.txt\n")
                    f.write(f"JumpBoosterAnim: anim/jump_boost/basic-enemy-turn.txt\n")
                for i in range(len(self.jump_boosters)):
                    f.write(f"JumpBooster: {i}" + "\n")
                    f.write(f"  position: ({round(self.jump_boosters[i].position[0] / 2, 1)}, {Components.map_size[1] - round(self.jump_boosters[i].position[1] / 2 - 1, 1) - 0.5})\n")
                    f.write(f"  min: ({round(self.jump_boosters[i].min[0] / 2, 1)}, {round(self.jump_boosters[i].min[1] / 2, 1)})\n")
                    f.write(f"  max: ({round(self.jump_boosters[i].max[0] / 2, 1)}, {round(self.jump_boosters[i].max[1] / 2, 1)})\n")
    
                f.write(f"DashRechargeCount: {len(self.dash_recharge)}\n")
                for i in range(len(self.dash_recharge)):
                    f.write(f"DashRecharge: {i}" + "\n")
                    f.write(f"  position: ({round(self.dash_recharge[i].position[0] / 2, 1)}, {Components.map_size[1] - round(self.dash_recharge[i].position[1] / 2 - 1, 1) - 0.5})\n")
    '''


class ObjectManager:
    def __init__(self):
        self.objects = {
            "spawnPoint": {"class": SpawnPoint, "list": []},
            "vine": {"class": Vine, "list": []},
            "NPC": {"class": TalkableNPC, "list": []},
            "spike": {"class": Spike, "list": []},
            "enemy": {"class": BasicEnemy, "list": []},
            "jumpBooster": {"class": JumpBooster, "list": []},
            "dashRecharge": {"class": DashRecharge, "list": []},
        }
        self.colors = {
            "spawnPoint": ("#FF0000", 5),
            "vine": ("#B5E61D", 1),
            "NPC": ("#0000FF", 1),
            "spike": ("#FF0000", 1),
            "enemy": ("#FF00FF", 1),
            "jumpBooster": ("#FFFF00", 1),
            "dashRecharge": ("#0066FF", 5),
        }

    def get_object_types(self):
        return self.objects.keys()
    def add_object(self, obj_type, *args, **kwargs):
        if obj_type not in self.objects:
            raise ValueError(f"Unknown object type: {obj_type}")

        cls = self.objects[obj_type]["class"]
        obj = cls(*args, **kwargs)
        self.objects[obj_type]["list"].append(obj)

    def get_objects(self, obj_type):
        return self.objects[obj_type]["list"]

    def draw_all_objects(self, painter, scale_x, scale_y):
        from PyQt5.QtGui import QPen, QColor
        from PyQt5.QtCore import Qt, QPoint

        for obj_type, entry in self.objects.items():
            color, width = self.colors[obj_type]
            painter.setPen(QPen(QColor(color), width, Qt.SolidLine))
            for obj in entry["list"]:
                obj.draw(painter, scale_x, scale_y)

    def clear(self):
        for entry in self.objects.values():
            entry["list"].clear()

    def clear_object_type(self, obj_type):
        self.objects[obj_type]["list"].clear()


    def save_object_to_file(self, filename):
        with open(filename, "w") as f:
            for obj_type, entry in self.objects.items():
                f.write(f"{obj_type[0].upper() + obj_type[1:]}Count: {len(entry["list"])}" + "\n")
                if (len(entry["list"]) != 0):
                    entry["class"].class_specific_stuff(f)
                i = 0
                for obj in entry["list"]:
                    f.write(f"{obj_type[0].upper() + obj_type[1:]}: {i}" + "\n")
                    obj.save_to_file(f, Components.map_size[1])
                    i+=1



obj_manager = ObjectManager()