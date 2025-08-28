import os
import subprocess
import threading

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QColorDialog, QComboBox, QInputDialog, \
    QLabel

from components import Components
from objects_menu.object_menu import ObjectMenu


class MainMenu(QWidget):
    def __init__(self, winExtent):
        super().__init__()

        right_layout = QVBoxLayout()
        save_bttn = QPushButton("Save")
        save_bttn.clicked.connect(self.save)
        right_layout.addWidget(save_bttn)

        self.combo = QComboBox()
        self.combo.addItems(["blocks", "objects"])
        right_layout.addWidget(self.combo)
        self.combo.currentIndexChanged.connect(self.switch_canvas)


        self.objectMenu = ObjectMenu()
        right_layout.addLayout(self.objectMenu)

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
        elif canvas == "objects":
            Components.current_canvas = Components.object_canvas
            self.objectMenu.begin_setting_objects()
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
            subprocess.run(["python", "level_saver/png_to_scene.py", "canvas_output", "file", value])
            os.remove('canvas_output.png')
            os.remove('file.txt')
            print(f"finished saving to file: {value}.txt")

        thread = threading.Thread(target=task, args=(value,))
        thread.daemon = True
        thread.start()