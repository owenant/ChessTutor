import lichess.api
from lichess.format import PGN, PYCHESS

if __name__ == "__main__":
    
    user = lichess.api.user('gabi_bc84') 
    url = user.get('playing')
    id = url.split('/')[-2] 
    game = lichess.api.game(id)
    print(game.get('moves'))
    print(lichess.api.game(id,format=PGN))
    _=1