import os
import subprocess
import threading

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QColorDialog, QComboBox, QInputDialog

from components import Components
from decorations.decor_menu import DecorMenu
from objects_menu.object_menu import ObjectMenu


class MainMenu(QWidget):
    def __init__(self, winExtent):
        super().__init__()

        right_layout = QVBoxLayout()
        save_bttn = QPushButton("Save")
        save_bttn.clicked.connect(self.save)
        right_layout.addWidget(save_bttn)

        self.combo = QComboBox()
        self.combo.addItems(["blocks", "objects", "decorations"])
        right_layout.addWidget(self.combo)
        self.combo.currentIndexChanged.connect(self.switch_canvas)

        self.clear_blocks_bttn = QPushButton("Clear Blocks")
        self.clear_blocks_bttn.clicked.connect(Components.blocks_canvas.clear)
        right_layout.addWidget(self.clear_blocks_bttn)

        self.objectMenu = ObjectMenu()
        right_layout.addLayout(self.objectMenu)

        self.decorMenu = DecorMenu()
        right_layout.addLayout(self.decorMenu)

        right_layout.addStretch()

        self.color_picker = QColorDialog()
        self.color_picker.setOptions(QColorDialog.NoButtons)  # Hide OK/Cancel
        self.color_picker.currentColorChanged.connect(self.color_changed)
        right_layout.addWidget(self.color_picker)

        self.setFixedSize(winExtent[0] // 5, winExtent[1])
        self.setLayout(right_layout)
        Components.brush_color = Qt.white

    def color_changed(self, color):
        Components.brush_color = color

    def switch_canvas(self, index):
        canvas = self.combo.itemText(index)
        if canvas == "blocks":
            Components.current_canvas = Components.blocks_canvas
            self.objectMenu.end_setting_objects()
            self.decorMenu.end_setting_decors()
        elif canvas == "decorations":
            Components.current_canvas = Components.decor_canvas
            self.objectMenu.end_setting_objects()
            self.decorMenu.begin_setting_decors()
        elif canvas == "objects":
            Components.current_canvas = Components.object_canvas
            self.objectMenu.begin_setting_objects()
            self.decorMenu.end_setting_decors()
        else:
            print(canvas)

    def clearObjects(self):
        Components.object_canvas.clear()

    def save(self):
        pixmap = QPixmap(Components.get_canvas().size())

        Components.get_canvas().render(pixmap)

        scaled_pixmap = pixmap.scaled(
            QSize(Components.map_size[0], Components.map_size[1]),
            Qt.KeepAspectRatio,
            Qt.FastTransformation
        )
        value, ok = QInputDialog.getText(self, "save scene", "scene name:")
        scaled_pixmap.save('canvas_output.png')

        def task(value):
            Components.object_canvas.saveObjectsToFile("file.txt")
            Components.decor_canvas.savedecorsToFile("file.txt")
            subprocess.run(["python", "level_saver/png_to_scene.py", "canvas_output", "file", value])
            os.remove('canvas_output.png')
            os.remove('file.txt')
            print(f"finished saving to file: {value}.txt")

        thread = threading.Thread(target=task, args=(value,))
        thread.daemon = True
        thread.start()