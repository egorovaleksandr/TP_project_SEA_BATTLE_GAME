import itertools
import fieldpart
import cell
import game_session


class Field(object):
    def __init__(self, size):
        self.size = size
        self.map = [[cell.Cell.empty_cell for i in range(size)] for i in range(size)]
        self.radar = [[cell.Cell.empty_cell for i in range(size)] for i in range(size)]

    def GetFieldPart(self, element):
        if element == fieldpart.FieldPart.MAP:
            return self.map
        if element == fieldpart.FieldPart.RADAR:
            return self.radar

    def DrawField(self, element):
        field = self.GetFieldPart(element)
        for x in range(-1, self.size):
            for y in range(-1, self.size):
                if x == -1 and y == -1:
                    print("  ", end="")
                    continue
                if x == -1 and y >= 0:
                    print(y + 1, end=" ")
                    continue
                if x >= 0 and y == -1:
                    print(game_session.Game_session.letters[x], end='')
                    continue
                print(" " + str(field[x][y]), end='')
            print("")

    def AddShipToField(self, ship, element):
        field = self.GetFieldPart(element)
        x, y = ship.x, ship.y
        width, height = ship.width, ship.height
        for p_x, p_y in itertools.product(range(x, x + height), range(y, y + width)):
            field[p_x][p_y] = ship

    def IsShipWithinField(self, ship):
        return self.size - ship.height + 1 > ship.x >= 0 and self.size - ship.width + 1 > ship.y >= 0

    def CheckShipFits(self, ship, element):
        field = self.GetFieldPart(element)
        result = self.IsShipWithinField(ship)
        x, y = ship.x, ship.y
        width, height = ship.width, ship.height
        for p_x, p_y in itertools.product(range(x, x + height), range(y, y + width)):
            result = result and str(field[p_x][p_y]) != cell.Cell.miss_cell
        for p_x, p_y in itertools.product(range(x - 1, x + height + 1), range(y - 1, y + width + 1)):
            result = result and not (0 <= p_x < len(field) and 0 <= p_y < len(field) and
                                     str(field[p_x][p_y]) in (cell.Cell.ship_cell, cell.Cell.destroyed_ship))
        return result

    def MarkDestroyedShip(self, ship, element):
        field = self.GetFieldPart(element)
        x, y = ship.x, ship.y
        width, height = ship.width, ship.height
        for p_x, p_y in itertools.product(range(x - 1, x + height + 1), range(y - 1, y + width + 1)):
            if 0 <= p_x < len(field) and 0 <= p_y < len(field):
                field[p_x][p_y] = cell.Cell.miss_cell
        for p_x, p_y in itertools.product(range(x, x + height), range(y, y + width)):
            field[p_x][p_y] = cell.Cell.destroyed_ship
