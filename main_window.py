from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout
from base_block_canvas import BaseBlockCanvas
from components import Components
from menu import MainMenu
import components

import sys

from object_canvas import ObjectCanvas
from top_canvas import TopCanvas


class LevelEditor(QMainWindow):
    def __init__(self, canvasExtent):
        super().__init__()
        self.win_width = 1800
        self.win_height = 900
        win_extent = [self.win_width, self.win_height]

        # compute editor canvases  width, height
        aspect_ratio = canvasExtent[0]/ canvasExtent[1]
        proposed_width = win_extent[0]*4 // 5
        proposed_height = int(proposed_width / aspect_ratio)
        if not proposed_height<= win_extent[1]:
            proposed_height = win_extent[1]
            proposed_width = int(proposed_height * aspect_ratio)



        self.resize(self.win_width, self.win_height)
        self.setWindowTitle("rfct lvl editor")

        self.canvas = BaseBlockCanvas(canvasExtent, [proposed_width, proposed_height])
        self.object_canvas = ObjectCanvas(canvasExtent, [proposed_width, proposed_height])
        self.menu = MainMenu(win_extent)

        tc = TopCanvas([proposed_width, proposed_height])

        canvas_container = QWidget()
        canvas_container.setFixedSize(proposed_width, proposed_height)

        self.canvas.setParent(canvas_container)
        self.object_canvas.setParent(canvas_container)
        tc.setParent(canvas_container)

        self.canvas.move(0, 0)
        self.object_canvas.move(0, 0)
        tc.move(0, 0)

        main_layout = QHBoxLayout()
        main_layout.addWidget(canvas_container)
        main_layout.addWidget(self.menu)

        container = QWidget()
        self.setCentralWidget(container)
        container.setLayout(main_layout)



        # Components singleton setup
        Components.set_window(self)
        Components.set_menu(self.menu)
        Components.set_canvas(self.canvas)
        Components.object_canvas = self.object_canvas
        Components.current_canvas = self.canvas

        Components.map_size = canvasExtent
        Components.editor_map_size = [proposed_width, proposed_height]
        Components.editor_scale = [proposed_width / canvasExtent[0], proposed_height / canvasExtent[1]]


if __name__ == "__main__":
    app = QApplication([sys.argv[0]])

    lvl_width = -1
    lvl_height = -1
    for arg in sys.argv[1:]:  # skip the script name
        if arg.startswith('lvlWidth:'):
            try:
                lvl_width = int(arg.split(':', 1)[1])
            except ValueError:
                pass
        elif arg.startswith('lvlHeight:'):
            try:
                lvl_height = int(arg.split(':', 1)[1])
            except ValueError:
                pass
    if lvl_width!= -1 and lvl_height != -1:
        print(f"creating window: {lvl_width}x{lvl_height}")
        window = LevelEditor([lvl_width, lvl_height])
        window.show()
        sys.exit(app.exec_())
