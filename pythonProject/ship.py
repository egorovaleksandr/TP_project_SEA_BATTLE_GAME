import cell


class Ship:
    def __init__(self, size, x, y, rotation):
        self.size = size
        self.hp = self.size
        self.x = x
        self.y = y
        self.height = 1
        self.width = self.size
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
        if self.rotation != 0:
            self.width, self.height = self.height, self.width
