from components import Components
from objects_menu.line_gane_objects import *
from objects_menu.point_game_objects import *

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
                if (len(entry["list"]) != 0):
                    f.write(f"{obj_type[0].upper() + obj_type[1:]}Count: {len(entry["list"])}" + "\n")
                    entry["class"].class_specific_stuff(f)
                i = 0
                for obj in entry["list"]:
                    f.write(f"{obj_type[0].upper() + obj_type[1:]}: {i}" + "\n")
                    obj.save_to_file(f, Components.map_size[1])
                    i+=1

obj_manager = ObjectManager()