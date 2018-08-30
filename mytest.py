#!/usr/bin/env python
import traceback
from player_submission import OpenMoveEvalFn, CustomEvalFn, CustomPlayer
from isolation import Board, game_as_text
from test_players import RandomPlayer, HumanPlayer
import platform

if platform.system() != 'Windows':
    import resource
from time import time, sleep

try:
    """Example test to make sure
    your minimax works, using the
    OpenMoveEvalFunction evaluation function.
	This can be used for debugging your code
	with different model Board states. 
	Especially important to check alphabeta 
	pruning"""
    # create dummy 5x5 board
    b = Board(RandomPlayer(), HumanPlayer(), 5, 5)

    b.__board_state__ = [
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", "Q1", " "],
        [" ", " ", " ", "Q2", " "],
        [" ", " ", " ", " ", " "]
    ]
    b.__last_queen_move__[b.__queen_1__] = (2, 3, False)
    b.__last_queen_move__[b.__queen_2__] = (3, 3, False)
    b.move_count = 2

    output_b = b.copy()
    legal_moves = b.get_legal_moves()
    winner, move_history, termination = b.play_isolation(
        time_limit=100000, print_moves=True)
    print 'Minimax Test: Runs Successfully'
    # Uncomment to see example game
    # print game_as_text(winner, move_history, termination, output_b)
except NotImplementedError:
    print 'Minimax Test: Not Implemented'
except:
    print 'Minimax Test: ERROR OCCURRED'
    print traceback.format_exc()