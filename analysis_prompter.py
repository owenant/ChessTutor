import json
import chess.pgn

from gpt_utils import query_gpt, extract_json
from main_stockfish import StockFish, setup_board_state


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
    {color} to move.
    {pgn}
    
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
