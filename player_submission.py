#!/usr/bin/env python
from isolation import Board, game_as_text
from random import randint

# TODO: remove this time import later
import time

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
		# I'm the maximizing player. If the game's active player is not me, the legal moves are for the opponent,
		# and the "opponent" moves are actually for me
		if maximizing_player_turn:
			my_moves = game.get_legal_moves()
			opponent_moves = game.get_opponent_moves()
		else:
			my_moves = game.get_opponent_moves()
			opponent_moves = game.get_legal_moves()
		return float(len(my_moves) - len(opponent_moves))


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
		if maximizing_player_turn:
			my_moves = game.get_legal_moves()
			opponent_moves = game.get_opponent_moves()
		else:
			my_moves = game.get_opponent_moves()
			opponent_moves = game.get_legal_moves()

		if not my_moves:
			# Includes the case where there are no legal and opponent moves, since the active player has priority
			return float("-inf")
		if not opponent_moves:
			return float("inf")
		return float(2 * len(my_moves) - len(opponent_moves))


class CustomPlayer:
	"""Player that chooses a move using your evaluation function
	and a minimax algorithm with alpha-beta pruning.
	You must finish and test this player to make sure it properly
	uses minimax and alpha-beta to return a good move."""

	def __init__(self, search_depth=0, eval_fn=CustomEvalFn()):
		"""Initializes your player.

		if you find yourself with a superior eval function, update the default
		value of `eval_fn` to `CustomEvalFn()`

		Args:
			search_depth (int): The depth to which your agent will search. If search depth <= 0, it will search by
								 iterative deepening based on the time_left fn passed into the move() fn. Otherwise,
								 it will search to the specified depth
			eval_fn (function): Utility function used by your agent
		"""
		self.eval_fn = eval_fn
		self.search_depth = search_depth
		self.time_threshold = 15
		self.symm_threshold = 3
		self.boards_seen = BoardsSeen()

		self.count_leaves = 0

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
		start_move = time.time()
		search_fn = self.alphabeta

		if self.search_depth > 0:
			# Searching to a specified depth
			self.boards_seen = BoardsSeen() # Each time the player moves, boards seen will be reset, to force
											# the boards to be re-evaluated by searching deeper
			best_move, utility = search_fn(game, time_left, depth=self.search_depth)
		else:
			# Searching by iterative deepening
			start_k = time.time()
			best_move, utility = search_fn(game, time_left, depth=1) # Initialize best move by evaluating at level 1
			#print("Time taken to search at level 1: {}. Time left: {}".format(time.time() - start_k, time_left()))
			k = 2
			n = 2
			while time_left() > self.time_threshold:
				self.boards_seen = BoardsSeen() # Each time the player moves, boards seen will be reset, to force
												# the boards to be re-evaluated by searching deeper
				start_k = time.time()
				attempted_best_move, utility = search_fn(game, time_left, depth=k)
				if attempted_best_move is None:
					print("Time spent attempting level {} is {}".format(k, time.time() - start_k))
					break
				best_move = attempted_best_move
				n = k
				print("Time taken to search at level {}: {}".format(k, time.time() - start_k))
				k += 1
		print("Time taken to determine best move: {}".format(time.time() - start_move))
		return best_move

	def utility(self, game, maximizing_player):
		"""Can be updated if desired. Not compulsory. """
		return self.eval_fn.score(game, maximizing_player)

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
		print("Depth count = {}".format(depth))
		# BASE CASE: Lowest desired level reached
		if depth == 0:
			best_val = self.utility(game, maximizing_player)
			self.count_leaves += 1
			print("Final depth reached with board state below and value: {}".format(best_val))
			print("Maximizing player={}, {}'s turn to move".format(maximizing_player, game.get_active_players_queen()))
			print game.print_board()
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

			# BASE CASE: Forecasted game ends, so this child has no more children. Don't even have to look at anymore
			# children of the current node, because:
			# 1) If the AI is forecasted to win while the opponent plays "optimally", then we will always go down this
			# 	 path
			# 2) If the opponent is forecasted to win while the AI plays "optimally", then we will always avoid going
			# 	 down this path
			if is_over :
				if maximizing_player:
					print("{} wins by moving to {} (val: inf)".format(winner, legal_moves[i]))
					print game.print_board()
					return legal_moves[i], float("inf")
				else:
					print("{} wins by moving to {} (val: -inf)".format(winner, legal_moves[i]))
					print game.print_board()
					return legal_moves[i], float("-inf")

			# Forecasted game is not over, so continue to search this branch
			forecasted_best_move, forecasted_best_val = self.minimax(forecasted_game, time_left, depth-1, not maximizing_player)

			# If not enough time left, just return
			if time_left() <= 15:
				return None, None

			# The active player (self) tries to maximize the evaluated value, while the forecasted opponent
			# move tries to minimize the evaluated value
			if maximizing_player:
				if forecasted_best_val > best_val:
					best_val = forecasted_best_val
					best_move = legal_moves[i]
			else:
				if forecasted_best_val < best_val:
					best_val = forecasted_best_val
					best_move = legal_moves[i]

		print("Best move in this node for {} is {} with value {}".format(game.get_active_players_queen(), best_move, best_val))
		return best_move, best_val

	def alphabeta(self, game, time_left, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
		"""Implementation of the alphabeta algorithm

		Args:
			game (Board): A board and game state.
			time_left (function): Used to determine time left before timeout
			depth: Used to track how deep you are in the search tree
			alpha (float): Alpha value for pruning (upper threshold value from path to root)
			beta (float): Beta value for pruning (lower threshold value from path to root)
			maximizing_player (bool): True if maximizing player is active.

		Returns:
			(tuple, int): best_move, val
		"""
		game_state = game.get_state()
		# BASE CASE: Lowest desired level reached
		if depth == 0:
			best_val = self.utility(game, maximizing_player)
			return None, best_val

		best_move = None
		legal_moves = game.get_legal_moves()  # Legal moves for the active player
		if maximizing_player:	best_val = float("-inf")	# For a maximizing player, must be more than -inf
		else:					best_val = float("inf")		# For a minimizing player, must be less than inf
		for i in range(0,len(legal_moves)):
			# Forecast the game state with a move
			forecasted_game, is_over, winner = game.forecast_move(legal_moves[i])
			forecasted_game_state = forecasted_game.get_state()

			# BASE CASE: Forecasted game ends, so this child has no more children. Don't even have to look at anymore
			# children of the current node, because:
			# 1) If the AI is forecasted to win while the opponent plays "optimally", then we will always go down this
			# 	 path
			# 2) If the opponent is forecasted to win while the AI plays "optimally", then we will always avoid going
			# 	 down this path
			if is_over:
				if maximizing_player:
					return legal_moves[i], float("inf")
				else:
					return legal_moves[i], float("-inf")

			# BASE CASE: If forecasted board is symmetric with a board that has already been evaluated. Checking
			# symmetry if there are 3 moves or less on the board, since symmetry is rare with higher move count
			value_of_sym_board = None
			if forecasted_game.move_count <= self.symm_threshold:
				value_of_sym_board = self.boards_seen.get_symmetric_value(forecasted_game.get_state())
				if value_of_sym_board is not None:
					forecasted_best_val = value_of_sym_board
					forecasted_best_move = legal_moves[i]

			# Forecasted game is not over or already known, so continue to search this branch
			if forecasted_game.move_count > self.symm_threshold or value_of_sym_board is None:
				forecasted_best_move, forecasted_best_val = self.alphabeta(forecasted_game, time_left, depth-1,
																		   alpha, beta, not maximizing_player)

			# If not enough time left, just return
			if time_left() <= 15:
				return None, None

			# The active player (self) tries to maximize the evaluated value, while the forecasted opponent
			# move tries to minimize the evaluated value
			if maximizing_player:
				# Maximizing node: If I get a return value from a child that is >= beta, no need to look at further
				# children since I will never be returning a value that can replace beta
				if forecasted_best_val >= beta:
					if game.move_count <= self.symm_threshold:
						self.boards_seen.add(game.get_state(), best_val)
					return legal_moves[i], forecasted_best_val
				if forecasted_best_val > best_val:
					best_val = forecasted_best_val
					best_move = legal_moves[i]
				if forecasted_best_val > alpha:
					alpha = forecasted_best_val
			else:
				# Minimizing node: If I get a return value from a child that is <= alpha, no need to look at further
				# children since I will never be returning a value that can replace alpha
				if forecasted_best_val <= alpha:
					if game.move_count <= self.symm_threshold:
						self.boards_seen.add(game.get_state(), best_val)
					return legal_moves[i], forecasted_best_val
				if forecasted_best_val < best_val:
					best_val = forecasted_best_val
					best_move = legal_moves[i]
				if forecasted_best_val < beta:
					beta = forecasted_best_val

		if game.move_count <= self.symm_threshold:
			self.boards_seen.add(game.get_state(), best_val)
		return best_move, best_val


class BoardsSeen:
	"""
	A class containing the hash table of boards that have been seen, as well as the functions for checking for symmetry
	"""
	def __init__(self):
		self.boards_evaled = {}

	def add(self, board_state, board_value):
		self.boards_evaled[str(board_state)] = board_value # If the board already exists, it will update the value

	def get_exact_value(self, board_state):
		if str(board_state) in self.boards_evaled:
			return self.boards_evaled[str(board_state)]
		return None

	def get_symmetric_value(self, board_state):
		# Checking to see if there are symmetric boards that have already been evaluated. All the squares will be
		# covered by doing 3 rotations of the original board, then transposing the original board and rotating the
		# transposed board 3 times

		r_board_state = board_state
		tr_board_state = self.__transpose__(board_state)
		for i in range(0,4):
			if str(r_board_state) in self.boards_evaled:
				return self.boards_evaled[str(r_board_state)]
			if str(tr_board_state) in self.boards_evaled:
				return self.boards_evaled[str(tr_board_state)]
			r_board_state = self.__rotate_R__(r_board_state)
			tr_board_state = self.__rotate_R__(tr_board_state)
		return None

	def __vertical_flip__(self, matrix):
		return [row[::-1] for row in matrix]

	def __horizontal_flip__(self, matrix):
		return matrix[::-1]

	def __rotate_R__(self, matrix):
		# Rotating right is equivalent to reversing the order of the rows and then
		# taking the transpose. mat[::-1] reverses the order of the rows, and zip(*mat)
		# transposes the matrix. The output is a list of tuples, so map(list, mat) is
		# called to cast each tuple as a list
		return map(list, zip(*matrix[::-1]))

	def __transpose__(self, matrix):
		# *mat feeds each row of the matrix as separate arguments, and zip(*mat) takes
		# the first element of each row and puts it in a tuple. The result is a transposed
		# matrix as a list of tuples, so map(list, mat) is called to cast each tuple as
		# a list
		return map(list, zip(*matrix))