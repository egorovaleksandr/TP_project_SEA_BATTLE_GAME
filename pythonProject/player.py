import configuration
import game_session
import cell
import ship
import fieldpart
import state


class Player(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.message = []
        self.ships = []
        self.field = None

    def GetInput(self, input_type):
        if input_type == state.Input.PASS:
            print("Игрок ", self.name, ", введите пароль: ")
            is_correct = False
            while not is_correct:
                password = input()
                if password == self.password:
                    is_correct = True
                else:
                    print("Неправильный пароль, повторите попытку: ")
        if input_type == state.Input.REGISTRATION:
            print("Ведите имя игрока: ")
            self.name = input()
            is_correct = False
            while not is_correct:
                print("Придумайте пароль: ")
                self.password = input()
                print("Повторите пароль: ")
                password = input()
                if password == self.password:
                    is_correct = True
                else:
                    print("Пароли не совпадают, повторите попытку. ")
            print("Игрок \"{}\" успешно зарегистрирован. ".format(self.name))
        if input_type == state.Input.SHIP_SETUP:
            user_input = input().upper().replace(" ", "")
            if len(user_input) < 3:
                return [0, 0, 0]
            x, y, rotation = user_input[0], user_input[1:-1], user_input[-1]
            if x not in game_session.Game_session.letters or not y.isdigit() or\
                    int(y) not in range(1, game_session.Game_session.field_size + 1) or rotation not in ("H", "V"):
                self.message.append('Приказ непонятен, ошибка формата данных')
                return [0, 0, 0]
            return game_session.Game_session.letters.index(x), int(y) - 1, state.Rotation.HORIZONTAL if rotation == 'H' else state.Rotation.VERTICAL
        if input_type == state.Input.SHOT:
            user_input = input().upper().replace(" ", "")
            x, y = user_input[0].upper(), user_input[1:]
            if x not in game_session.Game_session.letters or not y.isdigit() or\
                    int(y) not in range(1, game_session.Game_session.field_size + 1):
                self.message.append('Приказ непонятен, ошибка формата данных')
                return configuration.INDICATOR, 0
            x_ind = game_session.Game_session.letters.index(x)
            y_ind = int(y) - 1
            return x_ind, y_ind

    def CheckPass(self):
        self.GetInput(state.Input.PASS)

    def MakeShot(self, target_player):
        sx, sy = self.GetInput(state.Input.SHOT)
        if sx + sy == configuration.INDICATOR or self.field.radar[sx][sy] != cell.Cell.empty_cell:
            return state.Result.RETRY
        shot_res = target_player.ReceiveShot((sx, sy))
        if shot_res == state.Result.MISS:
            self.field.radar[sx][sy] = cell.Cell.miss_cell
        if shot_res == state.Result.GET:
            self.field.radar[sx][sy] = cell.Cell.damaged_ship
        if type(shot_res) == ship.Ship:
            destroyed_ship = shot_res
            self.field.MarkDestroyedShip(destroyed_ship, fieldpart.FieldPart.RADAR)
            shot_res = state.Result.KILL
        return shot_res

    def ReceiveShot(self, shot):
        sx, sy = shot
        if str(self.field.map[sx][sy]) != cell.Cell.ship_cell:
            self.field.map[sx][sy] = cell.Cell.miss_cell
            return state.Result.MISS
        tmp_ship = self.field.map[sx][sy]
        if tmp_ship.hp <= 1:
            self.field.MarkDestroyedShip(tmp_ship, fieldpart.FieldPart.MAP)
            self.ships.remove(tmp_ship)
            return tmp_ship
        tmp_ship.hp -= 1
        self.field.map[sx][sy] = cell.Cell.damaged_ship
        return state.Result.GET
