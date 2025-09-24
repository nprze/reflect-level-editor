from objects_menu.game_objects import PointGameObject

class SpawnPoint(PointGameObject):
    def __init__(self, position):
        super().__init__(position)
    def draw(self, painter, scale_x, scale_y):
        super().draw(painter, scale_x, scale_y)
    def save_to_file(self, file, y_minus):
        super().save_to_file(file, y_minus)


class BasicEnemy(PointGameObject):
    def __init__(self, position):
        super().__init__(position)
        self.min = (-0.5, -0.5)
        self.max = (0.5, 0.5)
        self.animation_name = "anim/enemy/basic-enemy-walk anim/enemy/basic-enemy-turn anim/enemy/basic-enemy-die"
    def draw(self, painter, scale_x, scale_y):
        top_left = self._scale_point((self.position[0] + self.min[0], self.position[1] + self.min[1]), scale_x, scale_y)
        top_right = self._scale_point((self.position[0] + self.max[0], self.position[1] + self.min[1]), scale_x,scale_y)
        bottom_right = self._scale_point((self.position[0] + self.max[0], self.position[1] + self.max[1]), scale_x,scale_y)
        bottom_left = self._scale_point((self.position[0] + self.min[0], self.position[1] + self.max[1]), scale_x,scale_y)
        painter.drawLine(top_left, top_right)
        painter.drawLine(top_right, bottom_right)
        painter.drawLine(bottom_right, bottom_left)
        painter.drawLine(bottom_left, top_left)

    def save_to_file(self, file, y_minus):
        super().save_to_file(file, y_minus)
        file.write(f"  min: ({round(self.min[0] / 2, 1)}, {round(self.min[1] / 2, 1)})\n")
        file.write(f"  max: ({round(self.max[0] / 2, 1)}, {round(self.max[1] / 2, 1)})\n")
        file.write(f"  animName: {self.animation_name}\n")



class JumpBooster(PointGameObject):
    def __init__(self, position):
        super().__init__(position)
        self.min = (-0.5, -0.5)
        self.max = (0.5, 0.5)

    @staticmethod
    def class_specific_stuff(file):
        file.write("JumpBoosterFile: anim/jump_boost/basic-enemy-walk.txt\n")
        file.write("JumpBoosterAnim: anim/jump_boost/basic-enemy-turn.txt\n")

    def draw(self, painter, scale_x, scale_y):
        top_left = self._scale_point((self.position[0] + self.min[0], self.position[1] + self.min[1]), scale_x, scale_y)
        top_right = self._scale_point((self.position[0] + self.max[0], self.position[1] + self.min[1]), scale_x,scale_y)
        bottom_right = self._scale_point((self.position[0] + self.max[0], self.position[1] + self.max[1]), scale_x,scale_y)
        bottom_left = self._scale_point((self.position[0] + self.min[0], self.position[1] + self.max[1]), scale_x,scale_y)
        painter.drawLine(top_left, top_right)
        painter.drawLine(top_right, bottom_right)
        painter.drawLine(bottom_right, bottom_left)
        painter.drawLine(bottom_left, top_left)

    def save_to_file(self, file, y_minus):
        super().save_to_file(file, y_minus)
        file.write(f"  min: ({round(self.min[0] / 2, 1)}, {round(self.min[1] / 2, 1)})\n")
        file.write(f"  max: ({round(self.max[0] / 2, 1)}, {round(self.max[1] / 2, 1)})\n")



class DashRecharge(PointGameObject):
    def __init__(self, position):
        super().__init__(position)
    def draw(self, painter, scale_x, scale_y):
        super().draw(painter, scale_x, scale_y)

    def save_to_file(self, file, y_minus):
        super().save_to_file(file, y_minus)