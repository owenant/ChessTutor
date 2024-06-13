from pgntofen import PgnToFen
from stockfish import Stockfish

if __name__ == "__main__":
    sf=Stockfish(path="C:\\Users\\Ruizhe\\Desktop\\stockfish\\stockfish-windows-x86-64-avx2.exe")
    sf.set_elo_rating(3000)
    pgnFormat = 'e4 e5 Nf3 Nc6 d4 exd4 Nxd4 Nf6 Nc3 Bb4 Qf3'
    converter = PgnToFen()
    FENString=converter.getFullFen()
    
    print(f'FEN: {FENString} | Valid: {sf.is_fen_valid(FENString)}')
    print(sf.get_top_moves(3))
    for move in pgnFormat.split(' '):
        converter.move(move)
        FENString=converter.getFullFen()+' 0 1'
        sf.set_fen_position(FENString)
        print(f'FEN: {FENString} | Valid: {sf.is_fen_valid(FENString)}')
        print(sf.get_top_moves(3))