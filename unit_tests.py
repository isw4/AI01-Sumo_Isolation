#!/usr/bin/env python
import traceback
from player_submission import OpenMoveEvalFn, CustomEvalFn, CustomPlayer, BoardsSeen
from isolation import Board, game_as_text
from test_players import RandomPlayer, HumanPlayer

def test_symmetric_search():
	unique_states = {}
	unique_states[1] = [
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", "Q1", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "]
	]
	unique_states[2] = [
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", "Q1", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "]
	]
	unique_states[3] = [
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", "Q1", " ", " "]
	]
	unique_states[4] = [
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", "Q1", " ", " ", " "],
		[" ", " ", " ", " ", " "]
	]
	unique_states[5] = [
		[" ", "Q1", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "]
	]
	unique_states[6] = [
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", "Q1"]
	]
	bs = BoardsSeen()
	for i in range(1,len(unique_states)+1):
		bs.add(unique_states[i], i)
	blank_board = [
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "],
		[" ", " ", " ", " ", " "]
	]
	for i in range(0,5):
		for j in range(0,5):
			blank_board[i][j] = "Q1"
			value = bs.get_symmetric_value(blank_board)
			if value is None:
				print("There is no symmetric board stored for this input:")
				print blank_board
				assert False
			blank_board[i][j] = " "


test_symmetric_search()