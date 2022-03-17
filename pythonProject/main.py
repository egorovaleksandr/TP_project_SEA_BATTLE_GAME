import os

class FieldPart(object):
    main = 'map'
    radar = 'radar'

class Cell(object):
    empty_cell = ' '
    ship_cell = '■'
    destroyed_ship = 'X'
    damaged_ship = '□'
    miss_cell = '•'

class Field(object):
    def __init__(self, size):
        self.size = size
        self.map = [[Cell.empty_cell for i in range(size)] for i in range(size)]
        self.radar = [[Cell.empty_cell for i in range(size)] for i in range(size)]

    def GetFieldPart(self, element):
        if element == FieldPart.main:
            return self.map
        if element == FieldPart.radar:
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
                    print(Game_session.letters[x], end='')
                    continue
                print(" " + str(field[x][y]), end='')
            print("")

    def CheckShipFits(self, ship, element):
        field = self.GetFieldPart(element)
        if ship.x + ship.height - 1 >= self.size or ship.x < 0 or ship.y + ship.width - 1 >= self.size or ship.y < 0:
            return False
        x = ship.x
        y = ship.y
        width = ship.width
        height = ship.height
        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                if str(field[p_x][p_y]) == Cell.miss_cell:
                    return False
        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                if str(field[p_x][p_y]) in (Cell.ship_cell, Cell.destroyed_ship):
                    return False
        return True

    def MarkDestroyedShip(self, ship, element):
        field = self.GetFieldPart(element)
        x, y = ship.x, ship.y
        width, height = ship.width, ship.height
        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                field[p_x][p_y] = Cell.miss_cell
        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                field[p_x][p_y] = Cell.destroyed_ship

    def AddShipToField(self, ship, element):
        field = self.GetFieldPart(element)
        x, y = ship.x, ship.y
        width, height = ship.width, ship.height
        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                field[p_x][p_y] = ship


class Player(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.message = []
        self.ships = []
        self.field = None

    def GetInput(self, input_type):
        if input_type == "password":
            print("Игрок ", self.name, ", введите пароль: ")
            while True:
                password = input()
                if password == self.password:
                    break
                print("Неправильный пароль, повторите попытку: ")
        if input_type == "registration":
            print("Ведите имя игрока: ")
            self.name = input()
            while True:
                print("Придумайте пароль: ")
                self.password = input()
                print("Повторите пароль: ")
                password = input()
                if password == self.password:
                    break
                print("Пароли не совпадают, повторите попытку. ")
            print("Игрок \"{}\" успешно зарегистрирован. ".format(self.name))
        if input_type == "ship_setup":
            user_input = input().upper().replace(" ", "")
            if len(user_input) < 3:
                return 0, 0, 0
            x, y, r = user_input[0], user_input[1:-1], user_input[-1]
            if x not in Game_session.letters or not y.isdigit() or int(y) not in range(1, Game_session.field_size + 1) or r not in ("H", "V"):
                self.message.append('Приказ непонятен, ошибка формата данных')
                return 0, 0, 0
            return Game_session.letters.index(x), int(y) - 1, 0 if r == 'H' else 1
        if input_type == "shot":
            user_input = input().upper().replace(" ", "")
            x, y = user_input[0].upper(), user_input[1:]
            if x not in Game_session.letters or not y.isdigit() or int(y) not in range(1, Game_session.field_size + 1):
                self.message.append('Приказ непонятен, ошибка формата данных')
                return 500, 0
            x = Game_session.letters.index(x)
            y = int(y) - 1
            return x, y

    def CheckPass(self):
        self.GetInput("password")

    def MakeShot(self, target_player):
        sx, sy = self.GetInput('shot')
        if sx + sy == 500 or self.field.radar[sx][sy] != Cell.empty_cell:
            return 'retry'
        shot_res = target_player.ReceiveShot((sx, sy))
        if shot_res == 'miss':
            self.field.radar[sx][sy] = Cell.miss_cell
        if shot_res == 'get':
            self.field.radar[sx][sy] = Cell.damaged_ship
        if type(shot_res) == Ship:
            destroyed_ship = shot_res
            self.field.MarkDestroyedShip(destroyed_ship, FieldPart.radar)
            shot_res = 'kill'
        return shot_res

    def ReceiveShot(self, shot):
        sx, sy = shot
        if type(self.field.map[sx][sy]) == Ship:
            ship = self.field.map[sx][sy]
            ship.hp -= 1
            if ship.hp <= 0:
                self.field.MarkDestroyedShip(ship, FieldPart.main)
                self.ships.remove(ship)
                return ship
            self.field.map[sx][sy] = Cell.damaged_ship
            return 'get'
        else:
            self.field.map[sx][sy] = Cell.miss_cell
            return 'miss'

class Ship:
    def __init__(self, size, x, y, rotation):
        self.size = size
        self.hp = size
        self.x = x
        self.y = y
        self.rotation = rotation
        self.SetRotation(rotation)

    def __str__(self):
        return Cell.ship_cell

    def SetPosition(self, x, y, r):
        self.x = x
        self.y = y
        self.SetRotation(r)

    def SetRotation(self, r):
        self.rotation = r
        if self.rotation == 0:
            self.width = self.size
            self.height = 1
        elif self.rotation == 1:
            self.width = 1
            self.height = self.size
        elif self.rotation == 2:
            self.y = self.y - self.size + 1
            self.width = self.size
            self.height = 1
        elif self.rotation == 3:
            self.x = self.x - self.size + 1
            self.width = 1
            self.height = self.size

class Game_session(object):
    letters = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
    ships_rules = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    field_size = len(letters)

    def __init__(self):
        self.players = []
        self.current_player = None
        self.next_player = None
        self.status = 'prepare'

    def StartGame(self):
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def StatusCheck(self):
        if self.status == 'prepare' and len(self.players) >= 2:
            self.status = 'in game'
            self.StartGame()
            return True
        if self.status == 'in game' and len(self.next_player.ships) == 0:
            self.status = 'game over'
            return True

    def AddPlayer(self, player):
        player.GetInput('registration')
        player.field = Field(Game_session.field_size)
        self.ShipsSetup(player)
        self.players.append(player)

    def ShipsSetup(self, player):
        for ship_size in Game_session.ships_rules:
            ship = Ship(ship_size, 0, 0, 0)
            while True:
                Game_session.Clean()
                player.field.DrawField(FieldPart.main)
                player.message.append('Куда поставить корабль длины {} (введите координату и ориентацию корабля- H/V): '.format(ship_size))
                for i in player.message:
                    print(i)
                player.message.clear()
                x, y, r = player.GetInput('ship_setup')
                if x + y + r == 0:
                    continue
                ship.SetPosition(x, y, r)
                if player.field.CheckShipFits(ship, FieldPart.main):
                    player.field.AddShipToField(ship, FieldPart.main)
                    player.ships.append(ship)
                    break
                player.message.append('Неправильная позиция!')

    def Draw(self):
        self.current_player.field.DrawField(FieldPart.main)
        self.current_player.field.DrawField(FieldPart.radar)
        for line in self.current_player.message:
            print(line)

    def SwitchPlayers(self):
        self.current_player, self.next_player = self.next_player, self.current_player
    @staticmethod
    def Clean():
        os.system('cls' if os.name == 'nt' else 'clear')

playing = True
while playing:
    game = Game_session()
    players = []
    players.append(Player(name='', password=''))
    players.append(Player(name='', password=''))
    while True:
        game.StatusCheck()
        if game.status == "prepare":
            game.AddPlayer(players.pop(0))
        if game.status == "in game":
            Game_session.Clean()
            game.current_player.message.append("Игрок {}, ваш ход: ".format(game.current_player.name))
            game.Draw()
            game.current_player.message.clear()
            result = game.current_player.MakeShot(game.next_player)
            if result == "miss":
                game.next_player.message.append("Промахнулся! ")
                game.next_player.CheckPass()
                game.SwitchPlayers()
                continue
            elif result == 'retry':
                game.current_player.message.append('Попробуйте еще раз!')
                continue
            elif result == 'get':
                game.current_player.message.append('Отличный выстрел, продолжайте!')
                game.next_player.message.append('Наш корабль попал под обстрел!')
                continue
            elif result == 'kill':
                game.current_player.message.append('Корабль противника уничтожен!')
                game.next_player.message.append('Наш корабль был уничтожен!')
                continue
        if game.status == 'game over':
            Game_session.Clean()
            game.next_player.field.DrawField(FieldPart.main)
            game.current_player.field.DrawField(FieldPart.main)
            print('Это был последний корабль игрока {}'.format(game.next_player.name))
            print('{} выиграл!'.format(game.current_player.name))
            break
    print("Играть ещё ? (Да / Нет)")
    ans = input().lower()
    if ans in {"no", "n", "not", "нет", "не", "н"}:
        playing = False
print('Спасибо за игру')
input('')
