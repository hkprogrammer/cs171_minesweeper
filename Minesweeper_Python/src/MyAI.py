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


class MyAI( AI ):
	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.rowDimension = rowDimension
		self.colDimension = colDimension
		self.totalMines = totalMines
		self.currentX = startX
		self.currentY = startY
		self.probabilityBoard = [[-1 for j in range(colDimension)] for i in range(rowDimension)] #records the probability of a square being a mine or safe.
		self.queue = [(startX,startY)]
		self.coveredTiles = (rowDimension * colDimension) + 1
		self.board = [[None for j in range(colDimension)] for i in range(rowDimension)]
		self.version = 1
		self.potentialNeighbors = [(-1,0),(-1,1),(-1,-1),(0,1),(0,-1),(1,0),(1,-1),(1,1)]
		self.previousStep = (startX,startY)
		self.visited = []
		self.flagQueue = []
		self.flagVisited = []
		# for x,y in self.potentialNeighbors:
		# 	if self.inBounds(startX+x,startY+y):
		# 		self.queue.append((startX+x,startY+y))
		# 		self.probabilityBoard[startY+y][startX+x] = 0
		

		

	def getAction(self, number: int) -> "Action Object":
		self.updateBoard(self.currentX, self.currentY, number)
		# for i in self.board:
		# 	print(i)
		# print(self.coveredTiles)
		# print(self.currentX, self.currentY)
		# print()
		# print(f"uncovered {self.coveredTiles} totalMines {self.totalMines}")
		if self.coveredTiles == self.totalMines:
			return Action(AI.Action.LEAVE)
		if self.version == 0:
			if number == 0:
				self.getActionZero()
			if number == 1:
				self.getActionOne()

			return Action(AI.Action.UNCOVER, self.currentX, self.currentY)
		elif self.version == 1:
			#using probability to calculate the potential safest square.
			return self.bfs(number)
			
		else:
			return Action(AI.Action.LEAVE)
	def bfs(self,number):
		
		lx,ly = self.previousStep
		print("Was on square ",lx+1,ly+1)
		
		if len(self.flagQueue) > 0:
			return self.executeFlag()
  
  
  
		# this gives the neighbors their number
		for x,y in self.potentialNeighbors:
			nx,ny = lx+x,ly+y
			if self.inBounds(nx,ny):
				
				if self.probabilityBoard[ny][nx] == "#":
					#square already discovered
					continue
				
				if number == 0:
					self.probabilityBoard[ny][nx] = 0
					if (nx,ny) not in self.visited and (nx,ny) not in self.queue:
						self.queue.append((nx,ny))
					continue
				if self.probabilityBoard[ny][nx] == 0:
					continue
				if self.probabilityBoard[ny][nx] == -1:
					# print(f"changed {ny},{nx} to {number}")
					self.probabilityBoard[ny][nx] = number
				else:
					self.probabilityBoard[ny][nx] += number
		self.prettyPrint()
		
  
		if len(self.queue) > 0:
			print("using bfs")
			cx,cy = self.queue.pop(0)
			
			
			# print(self.queue)
			# print(self.visited)
			print(f"original cx,cy: ",cx+1,cy+1)
			# while (cx,cy) in self.visited:
			# 	cx,cy = self.queue.pop(0)
			if len(self.queue) == 0 and self.probabilityBoard[cy][cx] == "#":
				return self.minVal(number,cx,cy)
   
			if len(self.queue) == 0 and self.probabilityBoard[cy][cx] > 0:
				1/0
				r = self.rescan(number,cx,cy)
				if r:
					#there are more stuff in self.queue
					cx,cy = self.queue.pop(0)
				else:
					return self.executeFlag()
				

			while self.probabilityBoard[cy][cx] == "#" or self.probabilityBoard[cy][cx] in self.visited:
				cx,cy = self.queue.pop(0)

			while self.probabilityBoard[cy][cx] > 0:
				if len(self.queue) >0:
					cx,cy = self.queue.pop(0)
				else:
					return self.minVal(number,cx,cy)
			print(f"modified cx,cy: ",cx+1,cy+1)
			if (cx,cy) not in self.visited:
				self.coveredTiles -= 1
			
			self.probabilityBoard[cy][cx] = "#"
			self.visited.append((cx,cy))
			for x,y in self.potentialNeighbors:
				nx,ny = cx+x,cy+y
				if self.inBounds(nx,ny):
					if self.probabilityBoard[ny][nx] == 0 or self.probabilityBoard[ny][nx] == -1:
						if (nx,ny) not in self.visited and (nx,ny) not in self.queue:
							self.queue.append((nx,ny))
			print("uncovering ",cx+1,cy+1)
			# print(self.queue)
			self.previousStep = (cx,cy)

			
			return Action(AI.Action.UNCOVER,cx,cy)
		else:
			return self.minVal(number)
			

	def executeFlag(self):
		print("USING execute FLAG")
		self.prettyPrint()
		cx,cy = self.flagQueue.pop(0)
		while (cx,cy) in self.flagVisited:
			cx,cy = self.flagQueue.pop(0)
		#cx cy is the square to flag
  
		self.flagVisited.append((cx,cy))
		self.visited.append((cx,cy))
		self.probabilityBoard[cy][cx] = "#"
		print("FLAGGING ",cx+1,cy+1)
		return Action(AI.Action.FLAG,cx,cy)
	
			
		
   
   
   
	def minVal(self,number,cx,cy):
		
		
     
		print("USING MINVAL")
		minVal = float("inf")
		minX,minY = None,None
		backups = []
		numberings = []
		for i in range(len(self.probabilityBoard)):
			for j in range(len(self.probabilityBoard[i])):
				if self.probabilityBoard[i][j] == "#":
					continue
				if self.probabilityBoard[i][j] == -1:
					backUpY = i	
					backUpX = j
					backups.append((backUpX,backUpY))
					continue
				if self.probabilityBoard[i][j] <= minVal:
					minY = i
					minX = j	
					minVal = self.probabilityBoard[i][j]
					numberings.append(minVal)
		
		if numberings.count(minVal) > 1:
			# there exist more than 1 potential square of the same number to be discovered
			r = self.rescan(number,cx,cy)
			if r:
				#there are more stuff in self.queue
				minX,minY = self.queue.pop(0)
				
			else:
				return self.executeFlag()

  
		if minX != None and minY != None:
			print(minX+1,minY+1)
			
			if len(backups) == 1:
				minX, minY = backups.pop(0)
   
   
			if (minX,minY) not in self.queue and (minX,minY) not in self.visited:
				if len(self.queue) == 0:
					self.queue.append((minX,minY))
				self.coveredTiles -=1
				self.previousStep = (minX,minY)
				self.probabilityBoard[minY][minX] = "#"
				self.visited.append((minX,minY))
				return Action(AI.Action.UNCOVER,minX,minY)

			else:
				pass
	
	def rescan(self,number,cx,cy) -> bool:
		print("Rescanning")
		for y in range(len(self.probabilityBoard)):
			for x in range(len(self.probabilityBoard[y])):
				if self.probabilityBoard[y][x] == "#" or self.probabilityBoard[y][x] == -1:
					continue
				cx,cy = x,y
				emptySquares = []
				flaggedSquares = []
				for x,y in self.potentialNeighbors:
					nx,ny = cx+x,cy+y
					if self.inBounds(nx,ny):
			
						if (nx,ny) not in self.visited and (nx,ny) not in self.flagQueue:
							emptySquares.append((nx,ny))
						elif (nx,ny) in self.flagVisited:
							flaggedSquares.append((nx,ny))
				
				#case 1
				# if number of flagged squares equal to the number, then all undiscovered are safe
				if len(flaggedSquares) == number:
					self.queue.extend(emptySquares)
					return True
				#case 2
				# if number equals to the the number of undiscovered, then all undiscovered are flags
				elif len(emptySquares) == number:
					self.flagQueue.extend(emptySquares)
					return False

		raise Exception

  
				
					
		
		
 
 
	def prettyPrint(self):
		print(" ",end="")
		for r in range(self.rowDimension - 1, -1, -1):
			print(str(r+1).ljust(2) + '|', end=" ")
			for c in range(self.colDimension):
				if self.probabilityBoard[r][c] == -1:
					print(". ",end=" ")
				elif self.probabilityBoard[r][c] == "#":
					print("V ",end = " ")
				else:
					print(f"{self.probabilityBoard[r][c]} ", end= " ")
			if (r != 0):
				print('\n', end=" ")
		column_label = "     "
		column_border = "   "
		for c in range(1, self.colDimension+1):
			column_border += "---"
			column_label += str(c).ljust(3)
		print("")
		print(column_border)
		print(column_label)
 
	def getActionZero(self):
		if self.isValidMove(self.currentX + 1, self.currentY):
			self.currentX += 1
		elif self.isValidMove(self.currentX, self.currentY + 1):
			self.currentY += 1
		elif self.isValidMove(self.currentX - 1, self.currentY):
			self.currentX -= 1
		elif self.isValidMove(self.currentX, self.currentY - 1):
			self.currentY -= 1
		else:
			self.scan()


	def getActionOne(self):
		# if tile above or below is a 0
		if (self.inBounds(self.currentX, self.currentY + 1) and self.board[self.currentX][self.currentY + 1] == 0) or (self.inBounds(self.currentX, self.currentY - 1) and self.board[self.currentX][self.currentY - 1] == 0):
			# move right
			if self.isValidMove(self.currentX + 1, self.currentY):
				self.currentX += 1
			# move left
			elif self.isValidMove(self.currentX - 1, self.currentY):
				self.currentX -= 1
			# if no valid move, scan
			else:
				self.scan()

		# if tile right or left is a 0
		elif (self.inBounds(self.currentX + 1, self.currentY) and self.board[self.currentX + 1][self.currentY] == 0) or (self.inBounds(self.currentX - 1, self.currentY) and self.board[self.currentX - 1][self.currentY] == 0):
			# move down
			if self.isValidMove(self.currentX, self.currentY + 1):
				self.currentY += 1
			# move up
			elif self.isValidMove(self.currentX, self.currentY - 1):
				self.currentY -= 1
			# if no valid move, scan
			else:
				self.scan()

		# if tile below is a 1
		elif (self.inBounds(self.currentX, self.currentY + 1) and self.board[self.currentX][self.currentY + 1] == 1):
			# move up
			if self.isValidMove(self.currentX, self.currentY - 1):
				self.currentY -= 1
			# if no valid move, scan
			else:
				self.scan()

		# if tile above is a 1
		elif (self.inBounds(self.currentX, self.currentY - 1) and self.board[self.currentX][self.currentY - 1] == 1):
			# move down
			if self.isValidMove(self.currentX, self.currentY + 1):
				self.currentY += 1
			# if no valid move, scan
			else:
				self.scan()

		# if tile right is a 1
		elif (self.inBounds(self.currentX + 1, self.currentY) and self.board[self.currentX + 1][self.currentY] == 1):
			# move left
			if self.isValidMove(self.currentX - 1, self.currentY):
				self.currentX -= 1
			# if no valid move, scan
			else:
				self.scan()

		# if tile left is a 1
		elif (self.inBounds(self.currentX - 1, self.currentY) and self.board[self.currentX - 1][self.currentY] == 1):
			# move right
			if self.isValidMove(self.currentX + 1, self.currentY):
				self.currentX += 1
			# if no valid move, scan
			else:
				self.scan()

		else:
			self.scan()


	def scan(self):
		# Scan for a covered tile with an adjacent zero
		for x in range(self.colDimension):
			for y in range(self.rowDimension):
				if self.board[x][y] is None and self.hasAdjacentZero(x, y):
					self.currentX = x
					self.currentY = y
					return
		
		# Scan for three in a row
		for x in range(self.colDimension - 2):
			for y in range(self.rowDimension):
				# if both to the right of a 1 are also 1s
				if self.board[x][y] == 1 and self.board[x+1][y] == 1 and self.board[x+2][y] == 1:
					if self.isValidMove(x, y - 1):
						self.currentX = x
						self.currentY = y - 1
						return
					elif self.isValidMove(x, y + 1):
						self.currentX = x
						self.currentY = y + 1
						return
					elif self.isValidMove(x + 2, y - 1):
						self.currentX = x + 2
						self.currentY = y - 1
						return
					elif self.isValidMove(x + 2, y + 1):
						self.currentX = x + 2
						self.currentY = y + 1
						return

		for x in range(self.colDimension):
			for y in range(self.rowDimension - 2):
				if self.board[x][y] == 1 and self.board[x][y+1] == 1 and self.board[x][y+2] == 1:
					if self.isValidMove(x - 1, y):
						self.currentX = x - 1
						self.currentY = y
						return
					elif self.isValidMove(x + 1, y):
						self.currentX = x + 1
						self.currentY = y
						return
					elif self.isValidMove(x - 1, y + 2):
						self.currentX = x - 1
						self.currentY = y + 2
						return
					elif self.isValidMove(x + 1, y + 2):
						self.currentX = x + 1
						self.currentY = y + 2
						return

		# If no specific pattern is found, select the first covered tile
		for x in range(self.colDimension):
			for y in range(self.rowDimension):
				if self.board[x][y] is None:
					self.currentX = x
					self.currentY = y
					return


	def updateBoard(self, x, y, val):
		if self.board[x][y] == None:
			self.board[x][y] = val
			self.coveredTiles -= 1
	

	def inBounds(self, x, y):
		if x < 0 or x >= self.colDimension:
			return False
		if y < 0 or y >= self.rowDimension:
			return False
		return True


	def isValidMove(self, x, y):
		if not self.inBounds(x, y):
			return False
		if self.board[x][y] != None:
			return False
		return True

	def hasAdjacentZero(self, x, y):
		adjacentTiles = [
			(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
			(x - 1, y),                 (x + 1, y),
			(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
		]

		for adjX, adjY in adjacentTiles:
			if self.inBounds(adjX, adjY) and self.board[adjX][adjY] == 0:
				return True
		
		return False

if __name__ == "__main__":
	MyAI(5,5,1,0,0)