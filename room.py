import random
from objects import *
from cmu_112_graphics import *


def appStarted(app):
    # "Up", "Right", "Down", "Left"
    app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    app.rows, app.cols, app.cellSize, app.margin = 20, 20, 20, 0 
    app.board = [ ["white"] *  app.cols for i in range(app.rows)]
    app.walls, app.wallsCoords = createWalls(app) 

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
    wallCount = 15
    wallsCoords = set()
    walls = set()
    while len(wallsCoords) < wallCount:
        wallRow, wallCol = random.randint(0,19), random.randint(0, 19)
        result = placeWall(app, wallRow, wallCol, app.board)
        if result != None:
            wallSet, wallSetCoords = result
            walls = walls.union(wallSet)
            wallsCoords = wallsCoords.union(wallSetCoords)
            print("here", walls)
    return walls, wallsCoords

# chooses a random row, col to place a wall
def placeWall(app, row, col, board):
        wallSetSize = 4
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        wallSet, wallSetCoords = set(), set()
        if checkCellEmpty(app, row, col, board):
            for _ in range(len(directions)):
                dir = random.choice(directions)
                wallList = checkEmptyFromDirection(app, row, col, board, dir, wallSetSize)
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
def checkEmptyFromDirection(app, row, col, board, dir, wallSetSize):
    drow, dcol = dir
    wallList = set()
    wallList.add( (row, col) )
    for i in range(wallSetSize):
        newRow = row + drow * i
        newCol = col + dcol * i
        print(newRow, newCol)
        if not checkCellEmpty(app, newRow, newCol, board): 
            return None
        wallList.add( (newRow, newCol) )
    return wallList

def checkCellEmpty(app, row, col, board):
    return (0 < row <= app.rows and 
            0 < col <= app.cols and
            board[row][col] == "white")

# draws one cell according to its row and col position
def drawCell(app, canvas, row, col, cellColor):
    x = app.margin + col * app.cellSize
    y = app.margin + row * app.cellSize
    canvas.create_oval(x, y, x + app.cellSize, y + app.cellSize,
                            fill=cellColor)
def drawWalls(app, canvas):
    for wall in app.walls:
        drawCell(app, canvas, wall.row, wall.col, wall.color)

def redrawAll(app, canvas):
    drawWalls(app, canvas)
    drawCell(app, canvas, 4, 4, "blue")

runApp(width=400, height=400)