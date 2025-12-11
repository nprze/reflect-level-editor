from components import Components
from decorations.decorations import TallGrass
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import Qt

class DecorManager:
    def __init__(self):
        self.decors = {
            "tallGrass": {"class": TallGrass, "list": []}
        }
        self.colors = {
            "tallGrass": ("#00FF00", 3),
        }

    def get_decor_types(self):
        return self.decors.keys()

    def add_decor(self, obj_type, *args, **kwargs):
        if obj_type not in self.decors:
            raise ValueError(f"Unknown object type: {obj_type}")

        cls = self.decors[obj_type]["class"]
        obj = cls(*args, **kwargs)
        self.decors[obj_type]["list"].append(obj)

    def get_decors(self, obj_type):
        return self.decors[obj_type]["list"]

    def draw_all_decors(self, painter, scale_x, scale_y):


        for obj_type, entry in self.decors.items():
            color, width = self.colors[obj_type]
            painter.setPen(QPen(QColor(color), width, Qt.SolidLine))
            for obj in entry["list"]:
                obj.draw(painter, scale_x, scale_y)

    def clear(self):
        for entry in self.decors.values():
            entry["list"].clear()

    def clear_decor_type(self, obj_type):
        self.decors[obj_type]["list"].clear()

    def save_decor_to_file(self, filename):
        with open(filename, "a") as f:
            for obj_type, entry in self.decors.items():
                if (len(entry["list"]) != 0):
                    f.write(f"{obj_type[0].upper() + obj_type[1:]}Count: {len(entry["list"])}" + "\n")
                    entry["class"].class_specific_stuff(f)
                i = 0
                for obj in entry["list"]:
                    f.write(f"{obj_type[0].upper() + obj_type[1:]}: {i}" + "\n")
                    obj.save_to_file(f, Components.map_size[1])
                    i += 1


decor_manager = DecorManager()