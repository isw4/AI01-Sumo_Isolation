#!/usr/bin/env python
from isolation import Board, game_as_text
from random import randint


# This file is your main submission that will be graded against. Do not
# add any classes or functions to this file that are not part of the classes
# that we want.


class OpenMoveEvalFn:

	def score(self, game, maximizing_player_turn=True):
		"""Score the current game state

		Evaluation function that outputs a score equal to how many
		moves are open for AI player on the board minus how many moves
		are open for Opponent's player on the board.
		Note:
			1. Be very careful while doing opponent's moves. You might end up
			   reducing your own moves.
			3. If you think of better evaluation function, do it in CustomEvalFn below.

			Args
				param1 (Board): The board and game state.
				param2 (bool): True if maximizing player is active.

			Returns:
				float: The current state's score. MyMoves-OppMoves.

			"""

		# TODO: finish this function!
		legal_moves = game.get_legal_moves()
		opponent_moves = game.get_opponent_moves()
		score = len(legal_moves) - len(opponent_moves)
		#print(type(score))
		return float(score)


class CustomEvalFn:
	def __init__(self):
		pass

	def score(self, game, maximizing_player_turn=True):
		"""Score the current game state

		Custom evaluation function that acts however you think it should. This
		is not required but highly encouraged if you want to build the best
		AI possible.

		Args
			game (Board): The board and game state.
			maximizing_player_turn (bool): True if maximizing player is active.

		Returns:
			float: The current state's score, based on your own heuristic.

		"""

		# TODO: finish this function!
		raise NotImplementedError


class CustomPlayer:
	# TODO: finish this class!
	"""Player that chooses a move using your evaluation function
	and a minimax algorithm with alpha-beta pruning.
	You must finish and test this player to make sure it properly
	uses minimax and alpha-beta to return a good move."""

	def __init__(self, search_depth, eval_fn=OpenMoveEvalFn()):
		"""Initializes your player.

		if you find yourself with a superior eval function, update the default
		value of `eval_fn` to `CustomEvalFn()`

		Args:
			search_depth (int): The depth to which your agent will search
			eval_fn (function): Utility function used by your agent
		"""
		self.eval_fn = eval_fn
		self.search_depth = search_depth

	def move(self, game, legal_moves, time_left):
		"""Called to determine one move by your agent

			Note:
				1. Do NOT change the name of this 'move' function. We are going to call
				the this function directly.
				2. Change the name of minimax function to alphabeta function when
				required. Here we are talking about 'minimax' function call,
				NOT 'move' function name.
				Args:
				game (Board): The board and game state.
				legal_moves (dict): Dictionary of legal moves and their outcomes
				time_left (function): Used to determine time left before timeout

			Returns:
				tuple: best_move
			"""

		print("AI making a move with depth {}".format(self.search_depth))
		best_move, utility = self.minimax(game, time_left, depth=self.search_depth)
		return best_move

	def utility(self, game, maximizing_player):
		"""Can be updated if desired. Not compulsory. """
		return self.eval_fn.score(game)

	def minimax(self, game, time_left, depth, maximizing_player=True):
		"""Implementation of the minimax algorithm

		Args:
			game (Board): A board and game state.
			time_left (function): Used to determine time left before timeout
			depth: Used to track how deep you are in the search tree
			maximizing_player (bool): True if maximizing player is active.

		Returns:
			(tuple, int): best_move, val
		"""
		# print("Depth count = {}".format(depth))
		if depth == 0:
			best_val = self.utility(game, maximizing_player)
			# print("Final depth reached with board state below and value: {}".format(best_val))
			# print game.print_board()
			return None, best_val

		best_move = None
		if maximizing_player:   best_val = float("-inf")    # For a maximizing player, must be more than -inf
		else:                   best_val = float("inf")     # For a minimizing player, must be less than inf
		legal_moves = game.get_legal_moves()                # Legal moves for the active player
		# print("Board state with {}'s move. Maximizing node = {}".format(game.get_active_players_queen(), maximizing_player))
		# print game.print_board(legal_moves)
		for i in range(0,len(legal_moves)):
			# Forecast the game state with a move
			forecasted_game, is_over, winner = game.forecast_move(legal_moves[i])

			# Forecasted game is over, so no need to continue down the branch or continue to other children
			if is_over and not maximizing_player:
				best_val = float("-inf")
				best_move = legal_moves[i]
				# print("{} wins by moving to {} (val: {})".format(winner, best_move, best_val))
				# print game.print_board()
				break
			elif is_over and maximizing_player:
				best_val = float("inf")
				best_move = legal_moves[i]
				# print("{} wins by moving to {} (val: {})".format(winner, best_move, best_val))
				# print game.print_board()
				break

			# Forecasted game is not over, so continue to search this branch
			forecasted_best_move, forecasted_best_val = self.minimax(forecasted_game, time_left, depth-1, not maximizing_player)

			# The player making the move now (self) tries to maximize the evaluated value, while a forecasted opponent
			# move tries to minimize the evaluated value
			if maximizing_player:
				if forecasted_best_val > best_val:
					best_val = forecasted_best_val
					best_move = legal_moves[i]
			else:
				if forecasted_best_val < best_val:
					best_val = forecasted_best_val
					best_move = legal_moves[i]

		# print("Best move in this node for {} is {} with value {}".format(game.get_active_players_queen(), best_move, best_val))
		return best_move, best_val

	def alphabeta(self, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
		"""Implementation of the alphabeta algorithm

		Args:
			game (Board): A board and game state.
			time_left (function): Used to determine time left before timeout
			depth: Used to track how deep you are in the search tree
			alpha (float): Alpha value for pruning
			beta (float): Beta value for pruning
			maximizing_player (bool): True if maximizing player is active.

		Returns:
			(tuple, int): best_move, val
		"""
		# TODO: finish this function!
		raise NotImplementedError
		return best_move, val
