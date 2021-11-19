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
    app.mode = "roomMode" # modes: mazeMode, roomMode, splashscreenMode
    app.cx, app.cy = app.width//2, app.height//2
    if app.mode == "splashscreenMode":
        app.splashscreen = loadSplashscreen(app)
        createButtons(app)

    app.player = Player()
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
        app.wallSprite = app.loadImage(r"Graphics/wall.jpg")
        app.board = [ ["white"] *  app.cols for i in range(app.rows)]
        app.roomEnemies = [ Enemy(5,5), Enemy(8,8) ]
        app.roomItems = []
        app.walls, app.wallsCoords = createWalls(app)


#########################################################
# SPLASHSCREEN MODE
#########################################################

def loadSplashscreen(app):
    bkgd = app.loadImage(r"Graphics/dungeon.jpg")
    imageWidth, imageHeight = bkgd.size
    imagecx, imagecy = imageWidth//2, imageHeight//2
    print(imagecx, imagecy) 
    cropCoords = imagecx-app.cx, imagecy-app.cy, imagecx+app.cx, imagecy+app.cy
    print(cropCoords)
    return bkgd.crop(cropCoords)

def drawSplashscreen(app, canvas):
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.splashscreen))

def createButtons(app):
    cx, cy = app.cx, app.cy * 2/3
    width, height = app.width/5, app.height/15
    app.startButton = cx-width, cy-height, cx+width, cy+height
    
def drawButtons(app, canvas):
    # start button, help button

    # bkgd = app.loadImage(r"Graphics/dungeon.jpg")
    # imageWidth, imageHeight = bkgd.size
    # imagecx, imagecy = imageWidth//2, imageHeight//2
    # canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.splashscreen))
    cx, cy = app.cx, app.cy * 2/3
    canvas.create_rectangle(app.startButton, fill="brown")
    canvas.create_text(cx, cy, text="Start Game", font="{Century Schoolbook}", fill="white")
    
def splashscreenMode_mousePressed(app, event):
    x0, y0, x1, y1 = app.startButton
    if x0 < event.x < x1 and y0 < event.y < y1:
        print("changed")
        app.mode = "mazeMode"

def splashscreenMode_redrawAll(app, canvas):
    drawSplashscreen(app, canvas)
    drawButtons(app, canvas)


#########################################################
# GENERAL FUNCTIONS
#########################################################

# returns the value of game dimensions
def gameDimensions():
    rows, cols, cellSize, margin = 20, 20, 20, 0 
    # game dimensions can be changed here
    return (rows, cols, cellSize, margin)

# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
# cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, node):
    row, col = node
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

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


# draw graph works
def drawGraph(app, canvas, graph):
    # graph is an instance of the Graph class
    unvisitedCells = set()
    startNode = (0,0)
    unvisitedCells.add(startNode)
    visitedCells = set()
    while len(unvisitedCells) > 0:
        node = unvisitedCells.pop()
        visitedCells.add(node)
        _, neighbours = getNeighbours(app, app.rows, app.cols, 
                            node[0], node[1], visitedCells)
        #print(neighbours)
        for neighbour in neighbours:
            #print(neighbour)
            # if neighbour does not have a connected edge to the node
            if (node not in graph.table or 
                neighbour not in graph.getNeighbours(node)):
                drawMazeWall(app, canvas, node, neighbour)
        unvisitedCells = set.union(neighbours, unvisitedCells)

# returns two coordinates to draw the walls
def drawMazeWall(app, canvas, node, neighbour):
    # node and neighbour are going to be in the format of (row, col)
    nodeRow, nodeCol = node
    neighbourRow, neighbourCol = neighbour
    if nodeRow == neighbourRow:
        if nodeCol > neighbourCol: # node is on the right of the neighbour
            x0, y0, x1, y1 = getCellBounds(app, node)
        else:  
            x0, y0, x1, y1 = getCellBounds(app, neighbour) # neighbour on right
        line = x0, y0, x0, y0 + app.cellSize
    elif nodeCol == neighbourCol:
        if nodeRow > neighbourRow: # node is on bottom of neighbour
            x0, y0, x1, y1 = getCellBounds(app, node)
        else:  # neighbour at bottom
            x0, y0, x1, y1 = getCellBounds(app, neighbour)
        line = x0, y0, x0 + app.cellSize, y0
    canvas.create_line(line)

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

#####################################################
# Drawing Functions
#####################################################

# draws one cell according to its row and col position
def drawCell(app, canvas, row, col, cellColor):
    x = app.margin + col * app.cellSize
    y = app.margin + row * app.cellSize
    canvas.create_oval(x, y, x + app.cellSize, y + app.cellSize,
                            fill=cellColor)

# draws every individual cell in the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
                cellColor = app.board[row][col]
                drawCell(app, canvas, row, col, cellColor) 

def drawRoomWalls(app, canvas):
    for wall in app.wallsCoords:
        x0, y0, x1, y1 = getCellBounds(app, wall)
        cx, cy = (x0+x1)//2, (y0+y1)//2
        wallSprite = app.wallSprite.resize( (int(x1-x0), int(y1-y0)) )
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(wallSprite))
        # drawCell(app, canvas, wall.row, wall.col, wall.color)

def drawBullets(app, canvas):
    for bullet in app.player.bullets:
        drawCell(app, canvas, bullet.row, bullet.col, "yellow")


def roomMode_redrawAll(app, canvas):
    # drawBoard(app, canvas)
    drawRoomWalls(app, canvas)
    # drawPlayer(app, canvas)
    # drawEnemies(app, canvas)
    # drawBullets(app, canvas)

runApp(width=800, height=600)