import os

import configuration
import state
import field
import fieldpart
import ship


class Game_session(object):
    letters = configuration.LETTERS
    ships_rules = configuration.SIZES
    field_size = len(letters)
    players_tmp = []
    finished = False
    preparing = state.Preparing
    ingame = state.InGame
    gameover = state.GameOver

    def __init__(self):
        self.players = []
        self.current_player = None
        self.next_player = None
        self.status = self.preparing

    def StartGame(self):
        self.current_player = self.players[0]
        self.next_player = self.players[1]

    def StatusCheck(self):
        if self.status == self.preparing and len(self.players) >= 2:
            self.status = self.ingame
            self.StartGame()
            return True
        if self.status == self.ingame and len(self.next_player.ships) == 0:
            self.status = self.gameover
            return True

    def AddPlayer(self, player):
        player.GetInput(state.Input.REGISTRATION)
        player.field = field.Field(Game_session.field_size)
        self.ShipsSetup(player)
        self.players.append(player)

    def ShipsSetup(self, player):
        for ship_size in Game_session.ships_rules:
            tmp_ship = ship.Ship(ship_size, 0, 0, 0)
            is_done = False
            while not is_done:
                Game_session.Clean()
                player.field.DrawField(fieldpart.FieldPart.MAP)
                player.message.append(
                    'Куда поставить корабль длины {} (введите координату и ориентацию корабля- H/V): '.format(
                        ship_size))
                [print(i) for i in player.message]
                player.message.clear()
                x, y, rotation = player.GetInput(state.Input.SHIP_SETUP)
                if 0 == x and 0 == y and 0 == rotation:
                    continue
                tmp_ship.SetPosition(x, y, rotation)
                if player.field.CheckShipFits(tmp_ship, fieldpart.FieldPart.MAP):
                    player.field.AddShipToField(tmp_ship, fieldpart.FieldPart.MAP)
                    player.ships.append(tmp_ship)
                    is_done = True
                else:
                    player.message.append('Неправильная позиция!')

    def Draw(self):
        self.current_player.field.DrawField(fieldpart.FieldPart.MAP)
        self.current_player.field.DrawField(fieldpart.FieldPart.RADAR)
        for line in self.current_player.message:
            print(line)

    def SwitchPlayers(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    @staticmethod
    def Clean():
        os.system('cls' if os.name == 'nt' else 'clear')
