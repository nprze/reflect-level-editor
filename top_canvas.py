from PyQt5.QtWidgets import QWidget

from components import Components


class TopCanvas(QWidget):
    def __init__(self, windowExtent):
        super().__init__()
        self.setFixedSize(windowExtent[0], windowExtent[1])

    def mousePressEvent(self, event):
        Components.current_canvas.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        Components.current_canvas.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        Components.current_canvas.mouseReleaseEvent(event)

