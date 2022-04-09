import cell
import state


class Ship:
    def __init__(self, size, x, y, rotation):
        self.size = size
        self.hp = self.size
        self.x = x
        self.y = y
        self.rotation = rotation
        self.SetRotation(rotation)

    def __str__(self):
        return cell.Cell.ship_cell

    def SetPosition(self, x, y, rotation):
        self.x = x
        self.y = y
        self.SetRotation(rotation)

    def SetRotation(self, rotation):
        self.rotation = rotation
        self.width, self.height = self.size, 1
        if self.rotation == state.Rotation.VERTICAL:
            self.height, self.width = self.width, self.height
