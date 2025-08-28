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
        # only horizontal / vertical lines
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])

        if dx > dy:
            end = (end[0], start[1])
        else:
            end = (start[0], end[1])

        super().__init__(start, end)
        self.direction = direction
    def draw_spike(self, painter, scale_x, scale_y, point):
        painter.drawLine(self._scale_point((point.x() - 0.25, point.y()), scale_x, scale_y),
                         self._scale_point((point.x() + 0.25, point.y()), scale_x, scale_y))
        painter.drawLine(self._scale_point((point.x(), point.y()), scale_x, scale_y),
                         self._scale_point((point.x(), point.y() - 1), scale_x, scale_y))
    def draw(self, painter, scale_x, scale_y):
        for i in range(self.end[0] - self.start[0]):
            pt=  QPoint()
            pt.setX(self.start[0] + i)
            pt.setY(self.start[1])
            self.draw_spike(painter, scale_x, scale_y, pt)
