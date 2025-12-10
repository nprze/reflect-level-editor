from game_objects import PointGameObject

class TallGrass(PointGameObject):
    def __init__(self, position):
        super().__init__(position)
    def draw(self, painter, scale_x, scale_y):
        print(self.position)
        painter.drawLine(self._scale_point(self.position, scale_x, scale_y),
                         self._scale_point(self.position + {1, 0}, scale_x, scale_y))
    def save_to_file(self, file, y_minus):
        super().save_to_file(file, y_minus)