import random
import copy
from graph import *
from objects import *
from cmu_112_graphics import *


# generates a walls in sets of 4 blocks
def createWalls(app, board):
    wallCount = 50
    wallsCoords = set()
    walls = set()
    while len(wallsCoords) < wallCount:
        wallRow, wallCol = random.randint(0,19), random.randint(0, 19)
        result = placeWall(app, wallRow, wallCol, board, wallsCoords)
        if result != None:
            wallSet, wallSetCoords = result
            walls = walls.union(wallSet)
            wallsCoords = wallsCoords.union(wallSetCoords)
            # print("here", walls)
    return walls, wallsCoords


# Loosely referenced from word search: 
# http://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
     
# chooses a random row, col to place a wall
def placeWall(app, row, col, board, wallsCoords):
    wallSetSize = 4
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    wallSet, wallSetCoords = set(), set()
    if checkCellEmpty(app, row, col, board, wallsCoords):
        for _ in range(len(directions)):
            dir = random.choice(directions)
            wallList = checkEmptyFromDirection(app, row, col, 
                        board, dir, wallSetSize, wallsCoords)
            # print(wallList)
            if wallList != None:
                for (wallRow, wallCol) in wallList:
                    wallSetCoords.add( (wallRow, wallCol) )
                    wall = Wall(wallRow, wallCol)
                    wallSet.add(wall)
                # print("place", wallSet, wallSetCoords)
                return (wallSet, wallSetCoords)
    return None

# Loosely referenced from word search: 
# http://www.cs.cmu.edu/~112/notes/2d-list-case-studies.html
     
# determines if there is sufficient space for a set of wall
def checkEmptyFromDirection(app, row, col, board, dir, wallSetSize, wallsCoords):
    drow, dcol = dir 
    wallList = set()
    wallList.add( (row, col) )
    for i in range(-1, wallSetSize+2):
        newRow = row + drow * i
        newCol = col + dcol * i
        # print(newRow, newCol)
        if not checkCellEmpty(app, newRow, newCol, board, wallsCoords): 
            return None
        if i < wallSetSize: wallList.add( (newRow, newCol) )
    return wallList

# check if chosen cell and cells in 4 directions surrounding it are empty
def checkCellEmpty(app, row, col, board, wallsCoords):
    if (0 <= row < app.rows and # within bounds
        0 <= col < app.cols and (row, col) != (0,0)):
        if (row, col not in wallsCoords): # not a wall
            # no walls in 4 directions around it 
            for (drow, dcol) in app.directions:
                newRow, newCol = row+drow, col+dcol
                if (newRow, newCol) in wallsCoords:
                    return False
            return True
    return False

# room object for generating multiple rooms in maze mode
class Room(object):
    def __init__(self, app, roomNum, row, col, enemyCount):
        self.roomNum = roomNum
        self.row, self.col = row, col # position in maze

        self.board = [ ["white"] *  app.cols for i in range(app.rows)]

        if roomNum < 2:
            self.walls, self.wallsCoords = createWalls(app, self.board)
        else:
            _, self.wallsCoords = kruskal(app, option="room")

        self.roomGraph = createRoomGraph(app, self.wallsCoords)
        self.roomAllNodes = createAllNodes(app)

        self.occupiedCoords = copy.deepcopy(self.wallsCoords)
        self.occupiedCoords.add((app.player.row, app.player.col))

        self.roomEnemies = []
        for i in range(enemyCount):
            row, col = createObjectInRoom(app, self.occupiedCoords)
            self.roomEnemies.append(Enemy(row, col))
            self.occupiedCoords.add((row, col))
        for enemy in self.roomEnemies:
            targetRow, targetCol = app.player.row, app.player.col
            if self.roomEnemies.index(enemy) % 2 == 0:
                enemy.path = aStar(self.roomGraph, (enemy.row, enemy.col), 
                         (targetRow, targetCol), self.roomAllNodes)
            else:
                enemy.path = bfs(self.roomGraph, (enemy.row, enemy.col), 
                         (targetRow, targetCol) )
        
        self.enemyStepTime = 0.5

        row, col = createObjectInRoom(app, self.occupiedCoords)
        self.healthBooster = HealthBooster(row, col)
        self.occupiedCoords.add((row, col))

        row, col = createObjectInRoom(app, self.occupiedCoords)
        self.timeFreezer = TimeFreezer(row, col)
        self.occupiedCoords.add((row, col))

        row, col = createObjectInRoom(app, self.occupiedCoords)
        self.door = Door(row, col, self.roomNum) # to escape back 
        self.occupiedCoords.add((row, col))

        row, col = createObjectInRoom(app, self.occupiedCoords)
        self.invisibilityPotion = InvisibilityPotion(row, col)
        self.occupiedCoords.add((row, col))
