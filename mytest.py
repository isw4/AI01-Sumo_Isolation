#!/usr/bin/env python
import traceback
from player_submission import OpenMoveEvalFn, CustomEvalFn, CustomPlayer, BoardsSeen
from isolation import Board, game_as_text
from test_players import RandomPlayer, HumanPlayer


def simple_alpha_beta(depth, leaf_index=0, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
	b = 2 # branching factor
	print("\nAt depth: {}, alpha: {}, beta: {}".format(depth, alpha, beta))
	# At a leaf node
	if depth == 0:
		value = leaf_array[leaf_index]
		print("Leaf[{}]: {}".format(leaf_index, value))
		leaf_index += 1
		return None, value, leaf_index

	# At an internal node, I get alpha and beta from parent. Updating this alpha and beta here doesnt affect upstream
	# or other unrelated branches.
	best_move = None
	if maximizing_player: best_val = float("-inf")  # For a maximizing player, must be more than -inf
	else:                 best_val = float("inf")   # For a minimizing player, must be less than inf
	for i in range(0,b):
		forecasted_best_move, forecasted_best_val, leaf_index = alpha_beta(depth-1, leaf_index, alpha, beta, not maximizing_player)
		print("Returning from depth {} to depth {} with returned value {}".format(depth-1, depth, forecasted_best_val))

		# Try to maximize the evaluated value, while the forecasted opponent move tries to minimize the evaluated value
		if maximizing_player:
			# If I get a return value from a child that is >= beta, no need to look at further
			# children since I will never be returning a value that can replace beta
			if forecasted_best_val >= beta:
				print("Pretending to prune the next branch")
				# return best_move, forecasted_best_val, leaf_index
			if forecasted_best_val > best_val:
				print("(Max)Returned value > current best value of {}. Setting best_val for this node".format(best_val))
				best_val = forecasted_best_val
			if forecasted_best_val > alpha:
				print("Also better than alpha of {}. Setting alpha".format(alpha))
				alpha = forecasted_best_val
		else:
			# Minimizing node: If I get a return value from a child that is <= alpha, no need to look at further
			# children since I will never be returning a value that can replace alpha
			if forecasted_best_val <= alpha:
				print("Pretending to prune the next branch")
				# return best_move, forecasted_best_val, leaf_index
			if forecasted_best_val < best_val:
				print("(Min)Returned value < current best value of {}. Setting best_val for this node".format(best_val))
				best_val = forecasted_best_val
			if forecasted_best_val < beta:
				print("Also less than beta of {}. Setting beta".format(beta))
				beta = forecasted_best_val
	return best_move, best_val, leaf_index

def test_no_best_move():
	### TODO: There is no best move available for the CustomPlayer. Maybe try to implement a next best move
	# Below is the setup that causes the AI to be unable to select a function.
	# Using the normal eval function and minimax algorithm
	b = Board(CustomPlayer(6), HumanPlayer(), 3, 3)
	b.__board_state__ = [
		["Q1", " ", " "],
		[" ", " ", "Q2"],
		[" ", " ", " "]
	]
	b.__last_queen_move__[b.__queen_1__] = (0, 0, False)
	b.__last_queen_move__[b.__queen_2__] = (1, 2, False)
	b.move_count = 2
	winner, move_history, termination = b.play_isolation(time_limit=1000, print_moves=True)
	print winner
	print move_history
	print termination
	print("End no_best_move test")

def test_alphabeta():
	# For alpha beta pruning test
	b = Board(CustomPlayer(3), HumanPlayer(), 5, 5)
	b.__board_state__ = [
		["X", "X", "X", "X", "X"],
		["X", " ", "X", " ", "X"],
		["X", " ", " ", "Q1", "X"],
		["X", " ", " ", "Q2", "X"],
		["X", "X", "X", "X", "X"]
	]
	b.__last_queen_move__[b.__queen_1__] = (2, 3, False)
	b.__last_queen_move__[b.__queen_2__] = (3, 3, False)
	b.move_count = 2
	winner, move_history, termination = b.play_isolation(time_limit=1000000, print_moves=True)
	print winner
	print move_history
	print termination
	print("End alphabeta test")

def test_simple_alphabeta():
	move, value, leaf_index = simple_alpha_beta(4)
	print("Exited alpha beta with move {} and value {}".format(move, value))


# create dummy 5x5 board
#b = Board(RandomPlayer(), HumanPlayer(), 5, 5)

# b = Board(HumanPlayer(), CustomPlayer(3), 5, 5)
# b.__board_state__ = [
# 	[" ", " ", " ", " ", " "],
# 	[" ", " ", " ", " ", " "],
# 	[" ", " ", " ", "Q1", " "],
# 	[" ", " ", " ", "Q2", " "],
# 	[" ", " ", " ", " ", " "]
# ]
# b.__last_queen_move__[b.__queen_1__] = (2, 3, False)
# b.__last_queen_move__[b.__queen_2__] = (3, 3, False)
# b.move_count = 2
# winner, move_history, termination = b.play_isolation(time_limit=1000, print_moves=True)
# print winner
# print move_history
# print termination

leaf_array = [19, 15, 17, -13, 14, 6, -9, -2, -17, 19, -4, 5, 17, 7, -3, -17]

test_alphabeta()