#!/usr/bin/env python
import traceback
from player_submission import OpenMoveEvalFn, CustomEvalFn, CustomPlayer
from isolation import Board, game_as_text
from test_players import RandomPlayer, HumanPlayer
import platform

if platform.system() != 'Windows':
    import resource
from time import time, sleep

print ""
try:
    sample_board = Board(RandomPlayer(), RandomPlayer())
    # setting up the board as though we've been playing
    sample_board.move_count = 2
    sample_board.__board_state__ = [
        ["Q1", " ", " ", " ", " ", " ", " "],
        [ " ", " ", " ", " ", " ", " ", " "],
        [ " ", " ", " ", " ", " ", " ", " "],
        [ " ", " ", " ","Q2", " ", " ", " "],
        [ " ", " ", " ", " ", " ", " ", " "],
        [ " ", " ", " ", " ", " ", " ", " "],
        [ " ", " ", " ", " ", " ", " ", " "]
    ]
    sample_board.__last_queen_move__ = {sample_board.__queen_1__: (0, 0, False), \
                                        sample_board.__queen_2__: (3, 3, False)}
    test = sample_board.get_legal_moves()
    print(len(test))
    opp_moves = sample_board.get_opponent_moves()
    print(len(opp_moves))
    h = OpenMoveEvalFn()
    print 'OpenMoveEvalFn Test: This board has a score of %s.' % (h.score(sample_board))
except NotImplementedError:
    print 'OpenMoveEvalFn Test: Not implemented'
except:
    print 'OpenMoveEvalFn Test: ERROR OCCURRED'
    print traceback.format_exc()