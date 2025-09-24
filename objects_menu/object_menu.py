from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QComboBox, QFrame
from components import Components
from objects_menu.object_manager import obj_manager

class ObjectMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.initialized = False

        self.combo = QComboBox()

        items = obj_manager.get_object_types()

        self.combo.addItems(items)
        self.combo.currentIndexChanged.connect(self.set_obj)
        self.addWidget(self.combo)
        self.combo.hide()

        self.clear_objs_bttn = QPushButton("Clear Objects")
        self.clear_objs_bttn.clicked.connect(self.clear_objs)
        self.addWidget(self.clear_objs_bttn)

        self.sep_line = QFrame()
        self.sep_line.setFrameShape(QFrame.HLine)
        self.sep_line.setFrameShadow(QFrame.Plain)
        self.addWidget(self.sep_line)

        self.clear_buttons = []
        for obj_name in obj_manager.get_object_types():
            button = QPushButton(f"clear {obj_name}")
            button.clicked.connect(self.clear_object_type)
            self.addWidget(button)
            self.clear_buttons.append(button)

        self.hide_all_clear_bttns()

    def begin_setting_objects(self):
        self.initialized = True
        self.show_all_clear_bttns()
        self.combo.show()

    def end_setting_objects(self):
        if (not self.initialized):
            return
        self.hide_all_clear_bttns()
        self.combo.hide()
        self.initialized = False

    def clear_objs(self):
        Components.object_canvas.clear()

    def clear_object_type(self):
        obj_manager.clear_object_type(self.sender().text()[6:])
        Components.object_canvas.update()

    def set_obj(self, index):
        objects = self.combo.itemText(index)
        Components.object_canvas.change_object_type(objects)

    def hide_all_clear_bttns(self):
        self.clear_objs_bttn.hide()
        self.sep_line.hide()
        for button in self.clear_buttons:
            button.hide()
    def show_all_clear_bttns(self):
        self.clear_objs_bttn.show()
        self.sep_line.show()
        for button in self.clear_buttons:
            button.show()