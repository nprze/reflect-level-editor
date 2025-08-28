from PyQt5.QtCore import QPoint

class GameObject:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, painter, scale_x, scale_y):
        raise NotImplementedError("draw method must be implemented by subclasses")

    def _scale_point(self, point, scale_x, scale_y):
        return QPoint(int(point[0] * scale_x), int(point[1] * scale_y))


class Vine(GameObject):
    def __init__(self, start, end, parts):
        super().__init__(start, end)
        self.parts = parts

    def draw(self, painter, scale_x, scale_y):
        painter.drawLine(self._scale_point(self.start, scale_x, scale_y),
                         self._scale_point(self.end, scale_x, scale_y))


class TalkableNPC(GameObject):
    def __init__(self, start, end, dialogue_name):
        super().__init__(start, end)
        self.dialogue_name = dialogue_name
        self.interaction_radius = 3

    def draw(self, painter, scale_x, scale_y):
        painter.drawLine(self._scale_point(self.start, scale_x, scale_y),
                         self._scale_point(self.end, scale_x, scale_y))


class Spike(GameObject):
    def __init__(self, start, end, direction):
        super().__init__(start, end)
        self.direction = direction

    def draw(self, painter, scale_x, scale_y):
        painter.drawLine(self._scale_point(self.start, scale_x, scale_y),
                         self._scale_point(self.end, scale_x, scale_y))
