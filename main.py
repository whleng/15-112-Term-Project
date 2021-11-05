# This is the main function 
# This is another comment

def function(x):
    return True
    
from cmu_112_graphics import *

class Player(object):
    def __init__(self):
        self.row, self.col = 0, 0

class Item(object):
    def __init__(self):
        pass

# returns the value of game dimensions
def gameDimensions():
    rows, cols, cellSize, margin = 15, 10, 20, 25 
    # game dimensions can be changed here
    return (rows, cols, cellSize, margin)

# draws every individual cell in the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
                cellColor = app.board[row][col]
                drawCell(app, canvas, row, col, cellColor) 

# draws one cell according to its row and col position
def drawCell(app, canvas, row, col, cellColor):
    x = app.margin + col * app.cellSize
    y = app.margin + row * app.cellSize
    canvas.create_rectangle(x, y, x + app.cellSize, y + app.cellSize)

def appStarted(app):
    app.player = Player()
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()

def keyPressed(app):
    arrowKeys = ["Up", "Right", "Down", "Left"]
    if event.key in arrowKeys:
        directions = [(0, -1), (0, 1), (1, 0), (0, -1)]
        drow = directions[arrowKeys.index(event.key)][0]
        dcol = directions[arrowKeys.index(event.key)][1]
        player.row += drow
        player.col += dcol

def timerFired(app):
    pass

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawPlayer(app, canvas)

runApp(width=400, height=400)