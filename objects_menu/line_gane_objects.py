from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QInputDialog, QDialog, QHBoxLayout, QPushButton

from game_objects import LineGameObject


class Vine(LineGameObject):
    def __init__(self, start, end):
        super().__init__(start, end)
        if (start[1]>end[1]):
            self.start = end
            self.end = start
        value, ok = QInputDialog.getInt(QInputDialog(), "vines", "input number of vines parts:", 14, 1, 100, 1)
        self.parts = 0
        if ok:
            self.parts = value

    def draw(self, painter, scale_x, scale_y):
        painter.drawLine(self._scale_point(self.start, scale_x, scale_y),
                         self._scale_point(self.end, scale_x, scale_y))

    def save_to_file(self, file, y_minus):
        super().save_to_file(file, y_minus)
        file.write(f"  edges: {self.parts}" + "\n")


class TalkableNPC(LineGameObject):
    def __init__(self, start, end):
        super().__init__(start, end)
        value, ok = QInputDialog.getText(QInputDialog(), "dialogue", "dialogue name")
        self.dialogue_name = ""
        if ok:
            self.dialogue_name = value
        self.interaction_radius = 3

    def draw(self, painter, scale_x, scale_y):
        super().draw(painter, scale_x, scale_y)

    def save_to_file(self, file, y_minus):
        super().save_to_file(file, y_minus)
        file.write(f"  interactionRadius: 3" + "\n")
        file.write(f"  dialogueName: {self.dialogue_name}" + "\n")



class Spike(LineGameObject):
    def orientation_dialogue(self, horizontal):
        dialog = QDialog()
        dialog.setWindowTitle("Two Buttons Dialog")

        clicked = {"value": None}

        def choose(value):
            clicked["value"] = value
            dialog.accept()

        layout = QHBoxLayout(dialog)

        right_text = "up"
        left_text = "down"
        if horizontal:
            right_text = "right"
            left_text = "left"
        left_btn = QPushButton(left_text)
        right_btn = QPushButton(right_text)

        left_btn.clicked.connect(lambda: choose(left_text))
        right_btn.clicked.connect(lambda: choose(right_text))

        layout.addWidget(left_btn)
        layout.addWidget(right_btn)

        dialog.exec_()
        return clicked["value"]


    def __init__(self, start, end):
        # only horizontal / vertical lines
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])

        if dx > dy:
            end = (end[0], start[1])
            if (start[0]>end[0]):
                helper = start
                start = end
                end = helper
            self.direction = self.orientation_dialogue(False)
        else:
            end = (start[0], end[1])
            if (start[1]<end[1]):
                helper = start
                start = end
                end = helper
            self.direction = self.orientation_dialogue(True)

        super().__init__(start, end)
    def draw_spike(self, painter, scale_x, scale_y, point):
        painter.drawLine(self._scale_point((point.x() - 0.25, point.y()), scale_x, scale_y),
                         self._scale_point((point.x() + 0.25, point.y()), scale_x, scale_y))
        painter.drawLine(self._scale_point((point.x(), point.y()), scale_x, scale_y),
                         self._scale_point((point.x(), point.y() - 1), scale_x, scale_y))
    def draw(self, painter, scale_x, scale_y):
        super().draw(painter, scale_x, scale_y)
        for i in range(self.end[0] - self.start[0]):
            pt=  QPoint()
            pt.setX(self.start[0] + i)
            pt.setY(self.start[1])
            self.draw_spike(painter, scale_x, scale_y, pt)

    def save_to_file(self, file, y_minus):
        super().save_to_file(file, y_minus)
        file.write(f"  dir: {self.direction}\n")

