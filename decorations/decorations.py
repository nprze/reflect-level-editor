from game_objects import PointGameObject

class TallGrass(PointGameObject):
    def __init__(self, position):
        super().__init__(position)
    def draw(self, painter, scale_x, scale_y):
        painter.drawLine(self._scale_point((self.position[0] - 0.25, self.position[1]), scale_x, scale_y),
                         self._scale_point((self.position[0] + 0.25, self.position[1]), scale_x, scale_y))
        painter.drawLine(self._scale_point((self.position[0], self.position[1]), scale_x, scale_y),
                         self._scale_point((self.position[0], self.position[1] - 1), scale_x, scale_y))
    def save_to_file(self, file, y_minus):
        self.position[1] += 0.5
        super().save_to_file(file, y_minus)
