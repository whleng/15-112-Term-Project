import random
from objects import *

def createWalls(app):
    ## complete random generation of 1 wall block
    # walls = set()
    # wallsCoords = set()
    # for _ in range(10):
    #     wall = Wall(random.randint(0,19), random.randint(0, 19))
    #     walls.add(wall)
    #     wallsCoords.add((wall.row, wall.col))
    # return walls, wallsCoords

    ## group generation of wall
    wallCount = 10
    walls = set()
    wallsCoords = set()
    while len(walls) < wallCount:
        wallRow, wallCol = random.randint(0,19), random.randint(0, 19)
        wallSet, wallSetCoords = placeWall(wallRow, wallCol, app.board)
        if wallSet != None and wallSetCoords != None:
            walls.union(wallSet)
            wallsCoords.union(wallSetCoords)
    return walls, wallsCoords

def placeWall(row, col, board):
        wallSetSize = 4
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        wallSet, wallSetCoords = [], []
        if checkCellEmpty(row, col, board):
                for dir in directions:
                    wallList = checkEmptyFromDirection(row, col, board, dir, wallSetSize)
                    if wallList != None:
                        for (wallRow, wallCol) in wallList:
                            wallSetCoords.append( (wallRow, wallCol) )
                            wall = Wall(wallRow, wallCol)
                            wallSet.append(wall)
                        return (wallSet, wallSetCoords)
        return None
        # if there is nothing in four areas around it, then place wall in a random direction
        # place wall in a set of 4 
        
def checkCellEmpty(row, col, board):
    return board[row][col] == "white"

def checkEmptyFromDirection(row, col, board, dir, wallSetSize):
    drow, dcol = dir
    wallList = [(row, col)]
    for i in range(wallSetSize):
        newRow = row + drow * i
        newCol = col + dcol * i
        if not checkCellEmpty(newRow, newCol, board): 
            return None
        wallList.append( (newRow, newCol) )
    return wallList

