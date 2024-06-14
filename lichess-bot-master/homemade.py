"""
Some example classes for people who want to create a homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""
import chess
from chess.engine import PlayResult, Limit
import random
from lib.engine_wrapper import MinimalEngine
from lib.types import MOVE, HOMEMADE_ARGS_TYPE
import logging
from main_stockfish import StockFish
# from analysis_prompter import *
from pgntofen import PgnToFen
from lib.types import (ReadableType, ChessDBMoveType, LichessEGTBMoveType, OPTIONS_GO_EGTB_TYPE, OPTIONS_TYPE,
                       COMMANDS_TYPE, MOVE, InfoStrDict, InfoDictKeys, InfoDictValue, GO_COMMANDS_TYPE, EGTPATH_TYPE,
                       ENGINE_INPUT_ARGS_TYPE, ENGINE_INPUT_KWARGS_TYPE)
from typing import Optional, Union, TypedDict
from lib.config import load_config, Configuration
from lib import engine_wrapper, model, lichess, matchmaking
from analysis_prompter import *
import json



# Use this logger variable to print messages to the console or log files.
# logger.info("message") will always print "message" to the console or log file.
# logger.debug("message") will only print "message" if verbose logging is enabled.
logger = logging.getLogger(__name__)


class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""

    def __init__(self, commands: COMMANDS_TYPE, options: OPTIONS_GO_EGTB_TYPE, stderr: Optional[int],
                 draw_or_resign: Configuration, game: Optional[model.Game] = None, name: Optional[str] = None,
                 **popen_args: str) -> None:
        """
        Initialize the values of the engine that all homemade engines inherit.

        :param options: The options to send to the engine.
        :param draw_or_resign: Options on whether the bot should resign or offer draws.
        """
        super().__init__(commands,options,stderr, draw_or_resign)


# Bot names and ideas from tom7's excellent eloWorld video

class AITutor(ExampleEngine):
    """AI tutor, play a stockfish move and then propose top three Stockfish moves for the human player with GPT-4 explanations."""

    def __init__(self, commands: COMMANDS_TYPE, options: OPTIONS_GO_EGTB_TYPE, stderr: Optional[int],
                 draw_or_resign: Configuration, game: Optional[model.Game] = None, name: Optional[str] = None,
                 **popen_args: str) -> None:
        """
        Initialize the values of the engine that all homemade engines inherit.

        :param options: The options to send to the engine.
        :param draw_or_resign: Options on whether the bot should resign or offer draws.
        """
        super().__init__(commands,options,stderr, draw_or_resign)
        self.sf = StockFish(elo=3000)
        self.pgn = []
        self.first_move = True
        self.color = check_turn(self.pgn)
        self.str_pgn = format_pgn(self.pgn)
        self.fen = ''
        self.move_output = ''
        self.board_output = ''
        self.top_moves = []
        self.internal_board = chess.Board()
        

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        """"""
        #Make a move using stockfish
        self.sf.sf.set_fen_position(board.board_fen())
        move = self.sf.sf.get_best_move()
        move = chess.Move.from_uci(move)
        
        self.pgn.append(self.internal_board.san(board.move_stack[-1]))
        # print(self.internal_board.san(board.move_stack[-1]) )
        self.internal_board.push(board.move_stack[-1])
        self.pgn.append(self.internal_board.san(move))
        board.push(move)
        self.color = check_turn(self.pgn)
        self.str_pgn = format_pgn(self.pgn)
        # print(self.pgn)
        # print(self.str_pgn)
        # print(self.color)
        
        #Query Stockfish for the best moves the human player can make (according to stockfish) and store explanations for the moves using GPT-4
        self.fen = board.fen()
        self.top_moves = self.sf.get_top_moves(self.fen)
        self.top_moves = [board.san(chess.Move.from_uci(move)) for move in self.top_moves]
        board_prompt = board_analysis_prompt(self.str_pgn, self.color)
        self.board_output = extract_json(query_gpt(board_prompt))
        self.board_output = json.dumps(self.board_output, indent=4)
        move_prompt = move_analysis_prompt(self.str_pgn, self.color, self.top_moves)
        self.move_output = query_gpt(move_prompt)
        
        
        #Actually make the move
        return PlayResult(move, None)


class Alphabetical(ExampleEngine):
    """Get the first move when sorted by san representation."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        """Choose the first move alphabetically."""
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Get the first move when sorted by uci representation."""

    def search(self, board: chess.Board, *args: HOMEMADE_ARGS_TYPE) -> PlayResult:
        """Choose the first move alphabetically in uci representation."""
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)


class ComboEngine(ExampleEngine):
    """
    Get a move using multiple different methods.

    This engine demonstrates how one can use `time_limit`, `draw_offered`, and `root_moves`.
    """

    def search(self, board: chess.Board, time_limit: Limit, ponder: bool, draw_offered: bool, root_moves: MOVE) -> PlayResult:
        """
        Choose a move using multiple different methods.

        :param board: The current position.
        :param time_limit: Conditions for how long the engine can search (e.g. we have 10 seconds and search up to depth 10).
        :param ponder: Whether the engine can ponder after playing a move.
        :param draw_offered: Whether the bot was offered a draw.
        :param root_moves: If it is a list, the engine should only play a move that is in `root_moves`.
        :return: The move to play.
        """
        if isinstance(time_limit.time, int):
            my_time = time_limit.time
            my_inc = 0
        elif board.turn == chess.WHITE:
            my_time = time_limit.white_clock if isinstance(time_limit.white_clock, int) else 0
            my_inc = time_limit.white_inc if isinstance(time_limit.white_inc, int) else 0
        else:
            my_time = time_limit.black_clock if isinstance(time_limit.black_clock, int) else 0
            my_inc = time_limit.black_inc if isinstance(time_limit.black_inc, int) else 0

        possible_moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)

        if my_time / 60 + my_inc > 10:
            # Choose a random move.
            move = random.choice(possible_moves)
        else:
            # Choose the first move alphabetically in uci representation.
            possible_moves.sort(key=str)
            move = possible_moves[0]
        return PlayResult(move, None, draw_offered=draw_offered)
