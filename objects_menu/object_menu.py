from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QComboBox
from components import Components

class ObjectMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.initialized = False

        self.clear_objs_bttn = QPushButton("Clear Objects")
        self.clear_objs_bttn.clicked.connect(self.clear_objs)
        self.addWidget(self.clear_objs_bttn)
        self.clear_objs_bttn.hide()

        self.combo = QComboBox()
        self.combo.addItems(["vines", "player spawn point", "talkable npc", "spikes"])
        self.combo.currentIndexChanged.connect(self.set_obj)
        self.addWidget(self.combo)
        self.combo.hide()
    def begin_setting_objects(self):
        self.initialized = True

        self.clear_objs_bttn.show()
        self.combo.show()
    def end_setting_objects(self):
        if (not self.initialized):
            return
        self.clear_objs_bttn.hide()
        self.combo.hide()
        self.initialized = False
    def clear_objs(self):
        Components.object_canvas.clear()
    def set_obj(self, index):
        objects = self.combo.itemText(index)
        Components.object_canvas.change_object_type(objects)