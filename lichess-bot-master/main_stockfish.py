import chess

from config import STOCK_FISH_PATH
from pgntofen import PgnToFen
from stockfish import Stockfish

def setup_board_state(pgnFormat):
    converter = PgnToFen()
    FENString = converter.getFullFen()

    for move in pgnFormat.split(' '):
        converter.move(move)
        FENString = converter.getFullFen() + ' 0 1'
    return FENString


class StockFish:
    def __init__(self, elo=3000):
        self.sf = Stockfish(path=STOCK_FISH_PATH)
        self.sf.set_elo_rating(elo)

    def get_top_moves(self, FENString, num_moves=3):
        self.sf.set_fen_position(FENString)
        top_moves = self.sf.get_top_moves(num_moves)
        return [cm['Move'] for cm in top_moves]


if __name__ == "__main__":

    sf = StockFish()
    pgnFormat = 'e4 e5 Nf3 Nc6 d4 exd4 Nxd4 Nf6 Nc3 Bb4 Qf3'
    fen = setup_board_state(pgnFormat)
    top_moves = sf.get_top_moves(fen)

    pgnFormat = 'e4 e5'
    fen = setup_board_state(pgnFormat)
    top_moves = sf.get_top_moves(fen)




    sf = Stockfish(path=STOCK_FISH_PATH)
    sf.set_elo_rating(3000)
    pgnFormat = 'e4 e5 Nf3 Nc6 d4 exd4 Nxd4 Nf6 Nc3 Bb4 Qf3'
    converter = PgnToFen()
    FENString = converter.getFullFen()
    
    print(f'FEN: {FENString} | Valid: {sf.is_fen_valid(FENString)}')
    print(sf.get_top_moves(3))
    for move in pgnFormat.split(' '):
        converter.move(move)
        FENString = converter.getFullFen()+' 0 1'
        sf.set_fen_position(FENString)
        print(f'FEN: {FENString} | Valid: {sf.is_fen_valid(FENString)}')
        print(sf.get_top_moves(3))