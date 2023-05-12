# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import random


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.board = [[None]*colDimension]*rowDimension
		self.totalMines = totalMines
		self.coveredTiles = colDimension*rowDimension
		self.currentX = startX
		self.currentY = startY
		self.currentNumber = 0
  
		#assume uncovered at starX and startY
	

	def updateBoard(self, x, y, value) -> None:
		if x < self.rowDimension and y < self.colDimension:
			self.board[x][y] = value
			self.coveredTiles-=1
		
	def checkEndCondition(self) ->bool:
		if self.coveredTiles == self.totalMines:
			return True
		#and other losing conditions
		return False

	def moveCondition(self,new_x,new_y) -> bool:
		return not (0<=new_x < self.colDimension and 0<=new_y <self.rowDimension) or (self.board[new_y][new_x] == None)

	def getAction(self, number: int) -> "Action Object":
		
		
		if number == 0:
			# move anywhere in 8 directions in random
			new_x,new_y = -1,-1
			while self.moveCondition(new_x, new_y):
				direction = random.randint(0,4)
				new_x,new_y = self.currentX,self.currentY
				if direction == 0:
					#move right
					new_x +=1
				elif direction == 1: 
					#move up
					new_y -= 1
				elif direction == 2:
					#move left
					new_x -= 1
				else:
					#move down
					new_y += 1
		
		self.updateBoard(new_x,new_y,number)
  
  
		self.currentX,self.currentY = new_x, new_y
		return Action(AI.Action.UNCOVER, new_x, new_y)
		
	
  
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################


if __name__ == "__main__":
    MyAI(5,5,10,0,0)