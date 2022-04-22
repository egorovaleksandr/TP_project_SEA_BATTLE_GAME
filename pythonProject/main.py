import configuration
import game_session
import player

if __name__ == '__main__':
    playing = True
    while playing:
        game = game_session.Game_session()
        game.players_tmp = [player.Player(name='', password=''), player.Player(name='', password='')]
        while not game.finished:
            game.StatusCheck()
            game.status.MakeAMove(game)
        print("Играть ещё ? (Да / Нет)")
        ans = input().lower()
        if ans not in configuration.ANSWERS:
            playing = False
    print('Спасибо за игру')
    input('')
