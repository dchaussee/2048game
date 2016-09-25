#!/usr/bin/env python
#coding:utf-8
# Daisy Chaussee
# dac2183

from random import randint
from BaseAI import BaseAI
import time
import math

values = [2, 4]

class PlayerAI(BaseAI):

	# matrix borrowed from the link in the hw assignment on stackoverflow
	matrix = [[  10,    8,    7,    6.5],
 		 	  [  .5,   .7,    1,    3],
 		 	  [ -.5, -1.5, -1.8,   -2],
 		 	  [-3.8, -3.7, -3.5,   -3]]

	def getMove(self, grid):

		return self.minmax(grid)

	# minmax algorithm uses minplay and maxplay and alpha-beta pruning to find and return the best move
	def minmax(self, grid):

		moves = grid.getAvailableMoves()
		bestmove = moves[0]
		alpha = float('-inf')
		beta = float('inf')

		for m in moves:
			copy = grid.clone()
			copy.move(m)
	
			# use recursion and update alpha and bestmove variables
			score = self.minplay(copy, 0, alpha, beta)

			if score > alpha:
				bestmove = m
				alpha = score
		return bestmove

	def minplay(self, grid, depth, alpha, beta):

		if not grid.canMove() or depth >= 2:
			return self.evaluate(grid)
		
		cells = grid.getAvailableCells()
		bestmove = (0, 0)

		for current in cells: 
			copy = grid.clone()

			if copy.canInsert(current):
					for v in values:
						copy.setCellValue(current, v)
		
						# use recursion and update beta and bestmove variables
						score = self.maxplay(copy, depth+1, alpha, beta)

						if score < beta:
							bestmove = current
							beta = score
						if beta <= alpha:
							break 
		return beta

	def maxplay(self, grid, depth, alpha, beta):
		
		if not grid.canMove() or depth >= 2:
			return self.evaluate(grid) # should return the score

		moves = grid.getAvailableMoves()
		bestmove = moves[0]

		for m in moves:
			copy = grid.clone()
			copy.move(m)
			score = self.minplay(copy, depth+1, alpha, beta)

			if score > alpha:
				bestmove = m
				alpha = score

			if alpha >= beta:
				break
		return alpha

	# evaluate a grid based on ability to merge, number of empty cells, matrix, 
	def evaluate(self, grid):

		adjCount = 0 # count for adjacent cell values
		numEmpty = len(grid.getAvailableCells())
		evaluationScore = 0
		counter = 0

		# calculate adjacent cells and merge ability and add to score
		for x in range(grid.size):
			for y in range(grid.size):
				cell = grid.getCellValue((x, y))

				if cell == grid.getCellValue((x + 1, y)):
					adjCount += 1

				if cell == grid.getCellValue((x - 1, y)):
					adjCount += 1

				if cell == grid.getCellValue((x, y + 1)):
					adjCount += 1

				if cell == grid.getCellValue((x, y - 1)):
					adjCount += 1

		# multiply cell values by hardcoded matrix
		for x in range(grid.size):
			for y in range(grid.size):
				# multiply first cell (0, 0) times 10, second cell (0, 1) by 8
				counter += self.matrix[x][y] * grid.getCellValue((x, y))

		# to ensure that the difference between adjacent cells is small
		# subtract value from evaluationScore (if value is large, this is bad)
		maxVal = 0
		maxPos = (0, 0)
		value = 0
		for x in range(grid.size):
			for y in range(grid.size):
				cell = grid.getCellValue((x, y))

				if cell > maxVal:
					maxVal = cell
					maxPos = (x, y)

				if x < grid.size - 1:
					value += abs(cell - grid.getCellValue((x + 1, y)))
				if x > 0:
					value += abs(cell - grid.getCellValue((x - 1, y)))
				if y < grid.size - 1:
					value += abs(cell - grid.getCellValue((x, y + 1)))
				if y > 0:
					value += abs(cell - grid.getCellValue((x, y - 1)))


		evaluationScore = 800 * adjCount + 270 * numEmpty + counter - value

		# if the max tile is in the top left corner, increase score
		if maxPos == (0, 0):
			if evaluationScore > 0:
				evaluationScore *= 2

		return evaluationScore


		
