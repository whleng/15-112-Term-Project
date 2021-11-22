from cmu_112_graphics import *
from graph import *
from mazeMap import *
from room import *
from objects import *
from bossRoom import *
import time

#########################################################
# Variables

WIDTH = 1300
HEIGHT = 750

# returns the value of game dimensions
def gameDimensions():
    rows, cols, cellSize, margin = 20, 20, 30, 0 # 38, 65, 20, 0 
    # game dimensions can be changed here
    return (rows, cols, cellSize, margin)

#########################################################
# MAIN APP
#########################################################

def appStarted(app):
    app.mode = "roomMode" # modes: mazeMode, roomMode, bossMode, splashscreenMode
    app.cx, app.cy = app.width//2, app.height//2
    
    if app.mode == "splashscreenMode":
        app.splashscreen = loadSplashscreen(app)
        createButtons(app)
  
    app.startTime = time.time()
    app.arrowKeys = ["Up", "Right", "Down", "Left"]
    # "Up", "Right", "Down", "Left"
    app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.gridWidth  = app.width - 2*app.margin
    app.gridHeight = app.height - 2*app.margin
    app.cellWidth = app.cellSize
    app.cellHeight = app.cellSize
    # app.cellWidth = app.gridWidth / app.cols
    # app.cellHeight = app.gridHeight / app.rows

    app.player = Player()
    createPlayerSprites(app)

    # mazeMode    
    if app.mode == "mazeMode":
        
        # app.enemy = Enemy(5,5)
        app.graph = prim(app)
        app.path = bfs(app.graph, 
                    (app.enemy.row, app.enemy.col),
                    (app.player.row, app.player.col))

    # roomMode
    elif app.mode == "roomMode":
        app.wallSprite = app.loadImage(r"Graphics/wall.jpg")
        app.board = [ ["white"] *  app.cols for i in range(app.rows)]
        # app.roomEnemies = [ Enemy(5,5), Enemy(8,8) ]
        # while True:
        #     x, y = random.randint(0, app.rows-1), random.rand(0, app.cols-1)
        #     if (x,y) not in app.wallsCoords:
        #         app.enemy = Enemy(x,y)
        #         break
        app.roomItems = []
        app.walls, app.wallsCoords = createWalls(app)
        createEnemies(app)
        print("start graph")
        app.graph = createRoomGraph(app)
        print(app.graph.table)
        app.path = bfs(app.graph, (app.enemy.row, app.enemy.col),
                        (app.player.row, app.player.col) )
        print(app.path)
        app.enemySteps = 0

    elif app.mode == "bossMode":
        bossRoomInit(app)

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

# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
# cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, node):
    row, col = node
    x0 = app.margin + col * app.cellWidth
    x1 = app.margin + (col+1) * app.cellWidth
    y0 = app.margin + row * app.cellHeight
    y1 = app.margin + (row+1) * app.cellHeight
    return (x0, y0, x1, y1)

def isLegalMove(app, playerRow, playerCol, prevPlayerRow=None, prevPlayerCol=None):
    # if app.mode == "roomMode":
    #     return (0 <= playerRow < app.rows and
    #             0 <= playerCol < app.cols and
    #             (playerRow, playerCol) not in app.wallsCoords)
    # elif app.mode == "mazeMode":
    if app.mode == "bossMode":
        return (0 <= playerRow < app.rows and
            0 <= playerCol < app.cols)
    else:
        return (playerRow, playerCol) in app.graph.getNeighbours((prevPlayerRow, prevPlayerCol))
    # return False

def convertDirections(app, dir):
    print(dir)
    if dir in app.directions: # in drow, dcol form
        return app.arrowKeys[app.directions.index(dir)]
    elif dir in app.arrowKeys: # in arrow key form
        return app.directions[app.arrowKeys.index(dir)]

def playerControls(app, event):
    app.playerSpriteCounter = (1 + app.playerSpriteCounter) % len(app.playerSprites[convertDirections(app, app.player.dir)])
    if event.key in app.arrowKeys:
        drow, dcol = convertDirections(app, event.key)
        playerRow = app.player.row + drow
        playerCol = app.player.col + dcol
        if isLegalMove(app, playerRow, playerCol, app.player.row, app.player.col):
            app.player.row = playerRow
            app.player.col = playerCol
            app.player.dir = (drow, dcol)
    elif event.key == "Space":
        app.player.attack()


# cited from 
# http://www.cs.cmu.edu/~112/notes/notes-graphics.html#installingModules
def createPlayerSprites(app):
    app.playerSprites = {'Left': [], 'Right': [], 'Up': [], 'Down': []} # "Up", "Right", "Down", "Left"
    # referenced from Tze Hng Loke (tloke)
    app.playerSpriteSheet = app.loadImage(r"Graphics/player.png")
    imageWidth, imageHeight = app.playerSpriteSheet.size
    app.playerHeightFactor = imageHeight / app.cellHeight 
    rows = 21
    cols = 13
    spriteRows = [9, 11, 8, 10]
    dirs = ["Left", "Right", "Up", "Down"]
    for row in range(4): # leftRow, rightRow, upRow, downRow 
        for col in range(cols):
            if col < 9: 
                spriteRow, dir = spriteRows[row], dirs[row]
                sprite = app.playerSpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*spriteRow, imageWidth/cols*(col+1) , imageHeight/rows*(spriteRow+1)))
                scaledsprite = app.scaleImage(sprite, app.playerHeightFactor)
                app.playerSprites[dir].append(scaledsprite)
        print(len(app.playerSprites[dir]))
    app.playerSpriteCounter = 0

def createEnemies(app):
    row, col = None, None
    while True: 
        if isLegalEnemy(app, row, col): break
        row, col = random.randint(0, app.rows), random.randint(0, app.cols)
    app.enemy = Enemy(row, col) 
    # should make it smartly generate not in a wall

def isLegalEnemy(app, row, col):
    return (row != None and col != None and
           0 <= row < app.rows and
           0 <= col < app.cols and
           (row, col) not in app.wallsCoords)

def drawPlayer(app, canvas):
    # draw player sprite
    sprite = app.playerSprites[convertDirections(app, app.player.dir)][app.playerSpriteCounter]
    x0, y0, x1, y1 = getCellBounds(app, (app.player.row, app.player.col) )
    cx, cy = (x0+x1)//2, (y0+y1)//2
    sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
    # # draw basic player
    # drawCell(app, canvas, app.player.row, app.player.col, app.player.color)

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
    enemy = app.enemy.row, app.enemy.col
    if currTime - app.startTime > 1:
        app.path = bfs(app.graph, enemy, player)
        app.path.pop()
        print(app.path)
        if app.path != []:
            app.enemy.row, app.enemy.col = app.path.pop()
            print("moved", app.enemy.row, app.enemy.col)
        # for enemy in app.roomEnemies:
        #    enemy.followPlayer(app.player.row, app.player.col)
        app.startTime = time.time()
    
def mazeMode_keyPressed(app, event):
    playerControls(app, event)

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
    enemy = app.enemy.row, app.enemy.col
    if app.enemySteps > 10:
        app.path = bfs(app.graph, enemy, player)
        app.path.pop()
        app.enemySteps = 0
    if currTime - app.startTime > 0.3:
        print("path: ", app.path)
        if app.path != []:
            app.enemySteps += 1
            app.enemy.row, app.enemy.col = app.path.pop()
            print("moved", app.enemy.row, app.enemy.col)
        # for enemy in app.roomEnemies:
        #    enemy.followPlayer(app.player.row, app.player.col)
        app.startTime = time.time()
    for bullet in app.player.bullets:
        print("bullet:", bullet)
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol
        # can't check collision because currently using single enemy instead of enemy list
        # app.roomEnemies = bullet.checkCollision(app.roomEnemies)

# should add some stuff 
def roomMode_keyPressed(app, event):
    playerControls(app, event)

#####################################################
# Drawing Functions
#####################################################

# draws one cell according to its row and col position
def drawCell(app, canvas, row, col, cellColor):
    x = app.margin + col * app.cellSize
    y = app.margin + row * app.cellSize
    canvas.create_rectangle(x, y, x + app.cellSize, y + app.cellSize,
                            fill=cellColor)

# draws every individual cell in the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
                cellColor = app.board[row][col]
                drawCell(app, canvas, row, col, cellColor) 

def drawRoomWalls(app, canvas):
    for wallCoord in app.wallsCoords:
        ## draw walls using sprite, need to loop through wall in wall coords
        x0, y0, x1, y1 = getCellBounds(app, wallCoord)
        cx, cy = (x0+x1)//2, (y0+y1)//2
        imageWidth, imageHeight = app.wallSprite.size
        scaleFactor =  (x1-x0) / imageWidth 
        print(scaleFactor)
        wallSprite = app.scaleImage(app.wallSprite, scaleFactor)
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(wallSprite))

        # draw wall as a circle, loop through wall in walls
        # drawCell(app, canvas, wall.row, wall.col, wall.color)

def drawBullets(app, canvas):
    for bullet in app.player.bullets:
        drawCell(app, canvas, bullet.row, bullet.col, "yellow")


def roomMode_redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawRoomWalls(app, canvas)
    drawPlayer(app, canvas)
    drawEnemies(app, canvas)
    drawBullets(app, canvas)


#########################################################
# BOSS MODE
#########################################################



def bossMode_keyPressed(app, event):
    # if event.key == "Space":
    #     app.gameEvent = "player attacks"
    # elif event.key == "Up":
    #     app.gameEvent = "player moves"
    # else:
    #     app.gameEvent = "player stops attack"
        
    app.arrowKeys = ["Up", "Right", "Down", "Left"]
    # "Up", "Right", "Down", "Left"
    app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    if event.key in app.arrowKeys:
        app.gameEvent = "player moves"
        drow, dcol = convertDirections(app, event.key)
        playerRow = app.player.row + drow
        playerCol = app.player.col + dcol
        if isLegalMove(app, playerRow, playerCol, app.player.row, app.player.col):
            app.player.row = playerRow
            app.player.col = playerCol
            app.player.dir = (drow, dcol)
            return
    elif event.key == "Space":
        app.player.attack()
        app.gameEvent = "player attacks"
        return

def bossMode_timerFired(app):
    app.boss.on_event(app, app.gameEvent)
    for bullet in app.player.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol
    for bullet in app.boss.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol

def bossMode_redrawAll(app, canvas):
    print(app.gameEvent)
    print(app.boss.x, app.boss.y)
    drawBoard(app, canvas)
    drawPlayer(app, canvas)
    drawBoss(app, canvas)
    drawBossRoomBullets(app, canvas)

runApp(width=WIDTH, height=HEIGHT)