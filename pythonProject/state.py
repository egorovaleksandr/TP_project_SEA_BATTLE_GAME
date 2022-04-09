from enum import Enum

import fieldpart
import game_session


class Input(Enum):
    PASS = 0
    REGISTRATION = 1
    SHIP_SETUP = 2
    SHOT = 3


class Result(Enum):
    MISS = 0
    RETRY = 1
    GET = 2
    KILL = 3


class State:
    def MakeAMove(game):
        return


class Preparing(State):
    def MakeAMove(game):
        game.AddPlayer(game.players_tmp.pop(0))


class InGame(State):
    def MakeAMove(game):
        game_session.Game_session.Clean()
        game.current_player.message.append("Игрок {}, ваш ход: ".format(game.current_player.name))
        game.Draw()
        game.current_player.message.clear()
        result = game.current_player.MakeShot(game.next_player)
        if result == Result.MISS:
            game.next_player.message.append("Промахнулся! ")
            game.next_player.CheckPass()
            game.SwitchPlayers()
        elif result == Result.RETRY:
            game.current_player.message.append('Попробуйте еще раз!')
        elif result == Result.GET:
            game.current_player.message.append('Отличный выстрел, продолжайте!')
            game.next_player.message.append('Наш корабль попал под обстрел!')
        elif result == Result.KILL:
            game.current_player.message.append('Корабль противника уничтожен!')
            game.next_player.message.append('Наш корабль был уничтожен!')


class GameOver(State):
    def MakeAMove(game):
        game_session.Game_session.Clean()
        game.next_player.field.DrawField(fieldpart.FieldPart.MAP)
        game.current_player.field.DrawField(fieldpart.FieldPart.MAP)
        print('Это был последний корабль игрока {}'.format(game.next_player.name))
        print('{} выиграл!'.format(game.current_player.name))
        game.finished = True
