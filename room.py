import random
from graph import *
from objects import *
from cmu_112_graphics import *

def appStarted(app):
    # "Up", "Right", "Down", "Left"
    app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    app.rows, app.cols, app.cellSize, app.margin = 20, 20, 20, 0 
    app.board = [ ["white"] *  app.cols for i in range(app.rows)]
    app.walls, app.wallsCoords = createWalls(app) 

def createRoomGraph(app):
    # using wall positions to create a graph
    graph = Graph()
    visited = set()
    for row in range(app.rows):
        for col in range(app.cols):
            cell = row, col
            if cell not in app.wallsCoords: # if the cell is not a wall
                _, neighbours = getNeighbours(app, app.rows, app.cols, row, col, set())
                for neighbour in neighbours: 
                    if neighbour not in app.wallsCoords: # if neighbour is not a wall
                        print("neighbour: ", neighbour)
                        graph.addEdge(cell, neighbour) 
    return graph


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
    wallCount = 50
    wallsCoords = set()
    walls = set()
    while len(wallsCoords) < wallCount:
        wallRow, wallCol = random.randint(0,19), random.randint(0, 19)
        result = placeWall(app, wallRow, wallCol, app.board, wallsCoords)
        if result != None:
            wallSet, wallSetCoords = result
            walls = walls.union(wallSet)
            wallsCoords = wallsCoords.union(wallSetCoords)
            print("here", walls)
    return walls, wallsCoords

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
                print(wallList)
                if wallList != None:
                    for (wallRow, wallCol) in wallList:
                        wallSetCoords.add( (wallRow, wallCol) )
                        wall = Wall(wallRow, wallCol)
                        wallSet.add(wall)
                    print("place", wallSet, wallSetCoords)
                    return (wallSet, wallSetCoords)
        return None
        
# determines if there is sufficient space for a set of wall
def checkEmptyFromDirection(app, row, col, board, dir, wallSetSize, wallsCoords):
    drow, dcol = dir 
    wallList = set()
    wallList.add( (row, col) )
    # currently ensures that at both ends of the walls there's enough space, but not in all 4 dir
    for i in range(-1, wallSetSize+2):
        newRow = row + drow * i
        newCol = col + dcol * i
        print(newRow, newCol)
        if not checkCellEmpty(app, newRow, newCol, board, wallsCoords): 
            return None
        if i < wallSetSize: wallList.add( (newRow, newCol) )
    return wallList

# need to improve this
def checkCellEmpty(app, row, col, board, wallsCoords):
    if (0 <= row < app.rows and # within bounds
        0 <= col < app.cols and (row, col) != (app.player.row, app.player.col)):
        if (row, col not in wallsCoords): # not a wall
            # no walls in 4 directions around it 
            for (drow, dcol) in app.directions:
                newRow, newCol = row+drow, col+dcol
                if (newRow, newCol) in wallsCoords:
                    return False
            return True
    return False
