from cmu_112_graphics import *
from graph import *
from mazeMap import *
from room import *
from objects import *
import time

#########################################################
# MAIN APP
#########################################################

def appStarted(app):
    app.player = Player()
    app.mode = "roomMode" # modes: mazeMode, roomMode, splashScreenMode
    app.startTime = time.time()
    # "Up", "Right", "Down", "Left"
    app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()

    # mazeMode
    if app.mode == "mazeMode":
        app.enemy = Enemy(5,5)
        app.graph = prim(app)
        app.path = dfs(app.graph, 
                    (app.enemy.row, app.enemy.col),
                    (app.player.row, app.player.col))

    # roomMode
    elif app.mode == "roomMode":
        app.board = [ ["white"] *  app.cols for i in range(app.rows)]
        app.roomEnemies = [ Enemy(5,5), Enemy(8,8) ]
        app.roomItems = []
        app.walls, app.wallsCoords = createWalls(app)

#########################################################
# GENERAL FUNCTIONS
#########################################################

# returns the value of game dimensions
def gameDimensions():
    rows, cols, cellSize, margin = 20, 20, 20, 0 
    # game dimensions can be changed here
    return (rows, cols, cellSize, margin)

def isLegalMove(app, playerRow, playerCol, prevPlayerRow=None, prevPlayerCol=None):
    if app.mode == "roomMode":
        if ((playerRow, playerCol) in app.wallsCoords or
         playerRow < 0 or playerRow >= app.rows or
         playerCol < 0 or playerCol >= app.cols):
            return False
        else: 
            return True
    elif app.mode == "mazeMode":
        if (playerRow, playerCol) in app.graph.getNeighbours((prevPlayerRow, prevPlayerCol)):
            return True
        else: 
            print("cant pass")
            return False
 
def drawPlayer(app, canvas):
    drawCell(app, canvas, app.player.row, app.player.col, app.player.color)

def drawEnemies(app, canvas):
    # temporarily having only 1 enemy
    enemy = app.enemy 
    drawCell(app, canvas, enemy.row, enemy.col, enemy.color)
    # for enemy in app.roomEnemies:
    #    drawCell(app, canvas, enemy.row, enemy.col, enemy.color)

# draws one cell according to its row and col position
def drawCell(app, canvas, row, col, cellColor):
    x = app.margin + col * app.cellSize
    y = app.margin + row * app.cellSize
    canvas.create_oval(x, y, x + app.cellSize, y + app.cellSize,
                            fill=cellColor)

#########################################################
# MAZE MODE
#########################################################

def mazeMode_timerFired(app):
    currTime = time.time()
    player = app.player.row, app.player.col
    print(player)
    enemy = app.enemy.row, app.enemy.col
    if currTime - app.startTime > 1:
        app.path = dfs(app.graph, enemy, player)
        app.path.pop()
        print(app.path)
        if app.path != []:
            app.enemy.row, app.enemy.col = app.path.pop()
            print("moved", app.enemy.row, app.enemy.col)
        # for enemy in app.roomEnemies:
        #    enemy.followPlayer(app.player.row, app.player.col)
        app.startTime = time.time()
    
def mazeMode_keyPressed(app, event):
    arrowKeys = ["Up", "Right", "Down", "Left"]
    if event.key in arrowKeys:
        drow = app.directions[arrowKeys.index(event.key)][0]
        dcol = app.directions[arrowKeys.index(event.key)][1]
        playerRow = app.player.row + drow
        playerCol = app.player.col + dcol
        if isLegalMove(app, playerRow, playerCol, app.player.row, app.player.col):
            app.player.row = playerRow
            app.player.col = playerCol
            app.player.dir = (drow, dcol)
    elif event.key == "Space":
        app.player.attack()

def mazeMode_redrawAll(app, canvas):
    drawGraph(app, canvas, app.graph)
    drawPlayer(app, canvas)
    drawEnemies(app, canvas)
    # for debugging path-finding of enemy
    # for (row, col) in app.path:
    #        drawCell(app, canvas, row, col, "red")
    

#########################################################
# ROOM MODE
#########################################################

def roomMode_timerFired(app):
    currTime = time.time()
    player = app.player.row, app.player.col
    print(player)
    enemy = app.enemy.row, app.enemy.col
    if currTime - app.startTime > 1:
        app.path = dfs(app.graph, enemy, player)
        app.path.pop()
        print(app.path)
        if app.path != []:
            app.enemy.row, app.enemy.col = app.path.pop()
            print("moved", app.enemy.row, app.enemy.col)
        # for enemy in app.roomEnemies:
        #    enemy.followPlayer(app.player.row, app.player.col)
        app.startTime = time.time()
    for bullet in app.player.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol
        app.roomEnemies = bullet.checkCollision(app.roomEnemies)

# should add some stuff 
def roomMode_keyPressed(app, event):
    arrowKeys = ["Up", "Right", "Down", "Left"]
    if event.key in arrowKeys:
        drow = app.directions[arrowKeys.index(event.key)][0]
        dcol = app.directions[arrowKeys.index(event.key)][1]
        playerRow = app.player.row + drow
        playerCol = app.player.col + dcol
        if isLegalMove(app, playerRow, playerCol):
            app.player.row = playerRow
            app.player.col = playerCol
            app.player.dir = (drow, dcol)
    elif event.key == "Space":
        app.player.attack()

# draws every individual cell in the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
                cellColor = app.board[row][col]
                drawCell(app, canvas, row, col, cellColor) 

def drawWalls(app, canvas):
    for wall in app.walls:
        drawCell(app, canvas, wall.row, wall.col, wall.color)

def drawBullets(app, canvas):
    for bullet in app.player.bullets:
        drawCell(app, canvas, bullet.row, bullet.col, "yellow")

def roomMode_redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawWalls(app, canvas)
    drawPlayer(app, canvas)
    drawEnemies(app, canvas)
    drawBullets(app, canvas)

runApp(width=400, height=400)