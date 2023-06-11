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
		self.numberBoard = [[-1 for j in range(colDimension)] for i in range(rowDimension)] 
		
		# self.originalNumberBoard = list(self.numberBoard)

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
		# print(self.flagQueue)
		
		
  
		lx,ly = self.previousStep

		self.numberBoard[ly][lx] = number if number >=0 else -2
		# self.originalNumberBoard = list(self.numberBoard)
		# print("Was on square ",lx+1,ly+1)
		
		if len(self.flagQueue) > 0:
			return self.executeFlag()
  
  
  
		# this gives the neighbors their number
		if number != -1:
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
						# self.probabilityBoard[ny][nx] += number
						self.probabilityBoard[ny][nx] += number
		
		print(self.queue)	

		if len(self.queue) > 0:
			
			cx,cy = self.queue.pop(0)
			
			
			# print(self.queue)
			# print(self.visited)
			# print("original cx,cy: ",cx+1,cy+1)
			# while (cx,cy) in self.visited:
			# 	cx,cy = self.queue.pop(0)
			if len(self.queue) == 0 and self.probabilityBoard[cy][cx] == "#":
				return self.minVal(number)
   
			if len(self.queue) == 0 and self.probabilityBoard[cy][cx] > 0:
				# r = self.rescan(number)
				# if r:
				# 	#there are more stuff in self.queue
				# 	cx,cy = self.queue.pop(0)
				# else:
				# 	return self.executeFlag()
				return self.minVal(number)
				
			
			

			while self.probabilityBoard[cy][cx] == "#" or self.probabilityBoard[cy][cx] in self.visited:
				cx,cy = self.queue.pop(0)

			while self.probabilityBoard[cy][cx] > 0:
				if len(self.queue) >0:
					cx,cy = self.queue.pop(0)
				else:
					return self.minVal(number)
			self.prettyPrint(self.probabilityBoard)
			self.prettyPrint(self.numberBoard)
			print("using bfs")
			print("modified cx,cy: ",cx+1,cy+1)
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
		self.prettyPrint(self.probabilityBoard)
		cx,cy = self.flagQueue.pop(0)
		print(f"atttempting to flag {cx+1}, {cy+1}")
		while (cx,cy) in self.flagVisited and len(self.flagQueue) > 0:
			cx,cy = self.flagQueue.pop(0)
			if len(self.flagQueue) == 0:
				raise AssertionError

		#cx cy is the square to flag
  
		self.flagVisited.append((cx,cy))
		self.visited.append((cx,cy))
		self.probabilityBoard[cy][cx] = "#"
		print("FLAGGING ",cx+1,cy+1)
		self.previousStep = (cx,cy)
		self.numberBoard[cy][cx] = -2
		
		print(self.probabilityBoard)
		for x,y in self.potentialNeighbors:
			nx,ny = cx+x,cy+y
			if self.inBounds(nx,ny):
				if self.probabilityBoard[ny][nx] == "#":
					continue
				if self.probabilityBoard[ny][nx] > 0:
					print(self.probabilityBoard[ny][nx])
					self.probabilityBoard[ny][nx] -= 1
					print(self.probabilityBoard[ny][nx])
		print(self.probabilityBoard)
  
  
  
		return Action(AI.Action.FLAG,cx,cy)
	
			
		
   
   
   
	def minVal(self,number):
		
		
		self.prettyPrint(self.probabilityBoard)
		self.prettyPrint(self.numberBoard)
		print("USING MINVAL")
		minVal = float("inf")
		minX,minY = None,None
		backups = []
		numberings = []
		numberingsPos = []
		foursToFlag = []
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
					numberingsPos.append((minX,minY))
				if self.probabilityBoard[i][j] >=3:
					#threshold
					foursToFlag.append((j,i))
		
		
  
  
		try:
			r = self.rescan(number)
			if r:
				#there are more stuff in self.queue
				minX,minY = self.queue.pop(0)
				print("will uncover ", minX+1, minY+1)
				
			else:
				print("will flag ", self.flagQueue[0][0]+1, self.flagQueue[0][1] + 1)
				return self.executeFlag()
		except Exception:
			#meaning no squres are able to be find from rescan
			pass


		if len(foursToFlag)>0:
			#flag these squares
			self.flagQueue.append(foursToFlag.pop(0))
			return self.executeFlag()
		
  
		if minX != None and minY != None:
			# print(minX+1,minY+1)
   
			if numberings.count(minVal) > 1:
				
				coords = []
				for i in range(len(numberings)):
					if numberings[i] == minVal:
						coords.append(numberingsPos[i])
				minX,minY = random.choice(coords)
				print(f"choosen random from ({minX}, {minY}) -> {coords}")
      
   
			if (minX,minY) not in self.queue and (minX,minY) not in self.visited:
				if len(self.queue) == 0:
					self.queue.append((minX,minY))
				self.coveredTiles -=1
				self.previousStep = (minX,minY)
				self.probabilityBoard[minY][minX] = "#"
				self.visited.append((minX,minY))
				self.previousStep = (minX,minY)
				return Action(AI.Action.UNCOVER,minX,minY)


		
		if len(backups) >= 1:
			print("using backups")
			#make a random move
			rInt = random.randint(0,len(backups)-1)
			minX, minY = backups.pop(rInt)
			if len(self.queue) == 0:
				self.queue.append((minX,minY))
			self.coveredTiles -=1
			self.previousStep = (minX,minY)
			self.probabilityBoard[minY][minX] = "#"
			self.visited.append((minX,minY))
			self.previousStep = (minX,minY)
			return Action(AI.Action.UNCOVER,minX,minY)
			
	
	def rescan(self,number=-1) -> bool:
		print("Rescanning")
		# print(self.numberBoard)
		for y in range(len(self.numberBoard)):
			for x in range(len(self.numberBoard[y])):
				

				if self.numberBoard[y][x] <= -1:
					continue
				
				
					
				cx,cy = x,y
				emptySquares = []
				flaggedSquares = []
				for zx,zy in self.potentialNeighbors:
					nx,ny = cx+zx,cy+zy
					if self.inBounds(nx,ny):
						if self.numberBoard[y][x] == 0:
							if (nx,ny) not in self.visited and (nx,ny) not in emptySquares:
								emptySquares.append((nx,ny))
								continue
						if (nx,ny) not in self.visited and (nx,ny) not in self.flagQueue and (nx,ny) not in emptySquares:
							emptySquares.append((nx,ny))
						elif (nx,ny) in self.flagVisited:
							flaggedSquares.append((nx,ny))
				
				#case 1
				# print(cx,cy)
				# print(emptySquares,flaggedSquares)
				# print(self.numberBoard[cy][cx])

				if len(emptySquares) == 0:
					continue
    
    
				# if number of flagged squares equal to the number, then all undiscovered are safe
				if len(flaggedSquares) == self.numberBoard[cy][cx]:
					self.queue.extend(emptySquares)
					# print(emptySquares)
					# print("using queue")
					# print(self.queue)
					# print(flaggedSquares)
					# print(emptySquares)
					# print("from ", cx+1,cy+1, "number = ", self.numberBoard[cy][cx])
					return True
				#case 2
				# if number equals to the the number of undiscovered, then all undiscovered are flags
				elif len(emptySquares) == self.numberBoard[cy][cx] - len(flaggedSquares):
					self.flagQueue.extend(emptySquares)
					# print("using flags")
					# print(self.flagQueue)
					# print(flaggedSquares)
					# print(emptySquares)
					# print("from ", cx+1,cy+1, "number = ", self.numberBoard[cy][cx])
					return False

		# return Action(AI.Action.LEAVE)
		raise Exception  
				
					
		
		
 
 
	def prettyPrint(self,board):
		print("printing out ", self.namestr(board,self.__dict__))
		print(" ",end="")
		for r in range(self.rowDimension - 1, -1, -1):
			print(str(r+1).ljust(2) + '|', end=" ")
			for c in range(self.colDimension):
				if board[r][c] == -1:
					print(". ",end=" ")
				elif board[r][c] == -2:
					print("F ",end=" ")
				elif board[r][c] == "#":
					print("/ ",end = " ")
				else:
					print(str(board[r][c]) + " ", end= " ")
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
  
	def namestr(self,obj, namespace):
		return [name for name in namespace if namespace[name] is obj]

 
 
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
		if self.board[y][x] == None:
			self.board[y][x] = val
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