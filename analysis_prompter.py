import json
from gpt_utils import query_gpt, extract_json
from main_stockfish import StockFish
import chess
from IPython.display import display, clear_output

# stockfish initialisation
sf = StockFish(elo=1500)
black_sf = StockFish(elo=1200)

# create new game for python chess
board = chess.Board()

pgn = []
while True:

    display(board)
    color = check_turn(pgn)
    str_pgn = format_pgn(pgn)

    # prompt = board_analysis_prompt(str_pgn, color)
    fen = board.fen()
    top_moves = sf.get_top_moves(fen)

    # query chatgpt
    board_prompt = board_analysis_prompt(str_pgn, color)
    move_prompt = move_analysis_prompt(str_pgn, color, top_moves)

    move_output = query_gpt(move_prompt)
    board_output = extract_json(query_gpt(board_prompt))
    # move_output = ''
    # board_output = []

    print("Here is an analysis of the board")
    print(json.dumps(board_output, indent=4))
    print("Here is some analysis of some potnetial moves")
    print(move_output)

    valid_move = False
    while not valid_move:
        player_move = input('Enter move: ')
        try:
            move = board.parse_san(player_move)
            if move in board.legal_moves:
                board.push(move)
                pgn.append(player_move)

                print(move)

                valid_move = True
            else:
                print("This move is not legal. Please try again.")
        except ValueError:
            print("Invalid move format or the move is not legal. Please try again.")

    # get FEN for updated board position
    fen = board.fen()
    # set stockfish position
    # ask stockfish for top 3 moves
    top_moves = black_sf.get_top_moves(fen, 1)

    # apply top stock fish move and re-render board
    stockfish_move = top_moves[0]
    san = board.push_san(stockfish_move)
    pgn.append(stockfish_move)
    clear_output()
    print(pgn)





def get_pgn_from_board(game):
    pgn = []
    board = game.board()
    for move in game.mainline_moves():
        san_move = board.san(move)
        pgn.append(san_move)
        # Make the move on the board to update its state
        board.push(move)
    return pgn


def format_pgn(list_pgn):
    pgn = ''
    for i, move in enumerate(list_pgn):

        turn = (i // 2) + 1
        if i % 2 == 0:
            pgn += str(turn) + '. ' + move
        else:
            pgn += ' ' + move + ' '
    return pgn

def check_turn(pgn):
    return 'Black' if len(pgn) % 2 == 1 else 'White'

def board_analysis_prompt(string_pgn, color):
    input_prompt = """
    This is the state of a chess game.
    {pgn}
    {color} to move.
    
    Provide an analysis of the board.
    Format the output with these sections:
    Material Balance
    King Safety
    Piece Activity
    Pawn Structure
    Immediate Threats
    
    Only output your response into json format. DO NOT provide any other output.
    """

    return input_prompt.format(pgn=string_pgn, color=color)


def move_analysis_prompt(string_pgn, color, moves):
    input_prompt = """
This is the state of a chess game.
{pgn}
{color} to move.
    
Provide an analysis of the following potential moves for {color}.
{str_moves}

Keep the analysis short for each move highlighting the most important aspects.
"""

    return input_prompt.format(pgn=string_pgn, color=color, str_moves='\n'.join(moves))


if __name__ == '__main__':
    # with open("data/pgns/guo_takahashi_2022.pgn", 'rb') as f:

    #game = chess.pgn.read_game(open("data/pgns/nn_philip_stamma_1737.pgn"))

    # with open("data/pgns/nn_philip_stamma_1737.pgn") as f:
    #     game = chess.pgn.read_game(f)
    #
    # turn_count = 1
    # pgn = get_pgn_from_board(game)[:turn_count]
    # print(pgn)
    pgn = ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'a6', 'Ba4', 'Nf6']

    color = check_turn(pgn)
    str_pgn = format_pgn(pgn)

    #prompt = board_analysis_prompt(str_pgn, color)
    sf = StockFish()
    fen = setup_board_state(' '.join(pgn))
    top_moves = sf.get_top_moves(fen)

    board_prompt = board_analysis_prompt(str_pgn, color)
    move_prompt = move_analysis_prompt(str_pgn, color, top_moves)


    move_output = query_gpt(move_prompt)
    board_output = extract_json(query_gpt(board_prompt))

    print(board_prompt)
    print()
    print(json.dumps(board_output, indent=4))
    print()
    print(move_prompt)
    print()
    print(move_output)
