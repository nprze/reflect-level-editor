from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QComboBox, QFrame
from components import Components
from decorations.decor_manager import decor_manager

class DecorMenu(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.initialized = False

        self.combo = QComboBox()

        items = decor_manager.get_decor_types()

        self.combo.addItems(items)
        self.combo.currentIndexChanged.connect(self.set_obj)
        self.addWidget(self.combo)
        self.combo.hide()

        self.clear_objs_bttn = QPushButton("Clear decors")
        self.clear_objs_bttn.clicked.connect(self.clear_objs)
        self.addWidget(self.clear_objs_bttn)

        self.sep_line = QFrame()
        self.sep_line.setFrameShape(QFrame.HLine)
        self.sep_line.setFrameShadow(QFrame.Plain)
        self.addWidget(self.sep_line)

        self.clear_buttons = []
        for obj_name in decor_manager.get_decor_types():
            button = QPushButton(f"clear {obj_name}")
            button.clicked.connect(self.clear_decor_type)
            self.addWidget(button)
            self.clear_buttons.append(button)

        self.hide_all_clear_bttns()

    def begin_setting_decors(self):
        self.initialized = True
        self.show_all_clear_bttns()
        self.combo.show()

    def end_setting_decors(self):
        if (not self.initialized):
            return
        self.hide_all_clear_bttns()
        self.combo.hide()
        self.initialized = False

    def clear_objs(self):
        Components.decor_canvas.clear()

    def clear_decor_type(self):
        decor_manager.clear_decor_type(self.sender().text()[6:])
        Components.decor_canvas.update()

    def set_obj(self, index):
        decors = self.combo.itemText(index)
        Components.decor_canvas.change_decor_type(decors)

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