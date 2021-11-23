from cmu_112_graphics import *
from graph import *
from mazeMap import *
from room import *
from objects import *
from bossRoom import *
from generalFunctions import *
import time

#########################################################
# Variables

WIDTH = 640
HEIGHT = 640

# returns the value of game dimensions
def gameDimensions():
    rows, cols, margin = 15, 15, 20 # 38, 65, 20, 0 
    # game dimensions can be changed here
    return (rows, cols, margin)

#########################################################
# MAIN APP
#########################################################

def appStarted(app):
    app.mode = "mazeMode" 
    # modes: mazeMode, roomMode, bossMode, splashscreenMode, winMode, loseMode
    app.cx, app.cy = app.width//2, app.height//2
    app.timerDelay = 10
    if app.mode == "splashscreenMode":
        app.splashscreen = loadSplashscreen(app)
        createButtons(app)
    
    app.winGame = None
    
    app.startTime = time.time()
    app.bfsStartTime = time.time()
    app.arrowKeys = ["Up", "Right", "Down", "Left"]
    # "Up", "Right", "Down", "Left"
    app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    app.rows, app.cols, app.margin = gameDimensions()
    app.gridWidth  = app.width - 2*app.margin
    app.gridHeight = app.height - 2*app.margin
    app.cellWidth = app.gridWidth/app.rows
    app.cellHeight = app.gridHeight/app.cols
    # app.cellWidth = app.gridWidth / app.cols
    # app.cellHeight = app.gridHeight / app.rows


    app.playerSpriteSheet = app.loadImage(r"Graphics/player.png")
    app.playerSprites = createMovingSprites(app, app.playerSpriteSheet, 
                    21, 13, range(8,12), 9)
    app.playerSpriteCounter = 0
    app.bulletSprite = app.loadImage(r"Graphics/bullets.png")
    app.bulletSprites = createObjectSprites(app, app.bulletSprite, 4, 4, 3)
    app.bulletSprites = app.bulletSprites[9:] # temporary fix  
    app.oneBulletSprite = app.loadImage(r"Graphics/oneBullet.png")
    app.doorSprite =  app.loadImage(r"Graphics/door.png")
    app.healthBoosterSprite = app.loadImage(r"Graphics/bullets.png")
    app.timeFreezerSprite = app.loadImage(r"Graphics/hourglass.png")

    if app.mode == "mazeMode":
        initMazeModeParams(app)
        initRoomModeParams(app)

    elif app.mode == "roomMode":
        initRoomModeParams(app)

    elif app.mode == "bossMode":
        initBossModeParams(app)
        

    bkgd = app.loadImage(r"Graphics/gameOver.jpg")
    imageWidth, imageHeight = bkgd.size
    imagecx, imagecy = imageWidth//2, imageHeight//2
    cropCoords = imagecx-app.cx, imagecy-app.cy, imagecx+app.cx, imagecy+app.cy
    app.loseModeImage =  bkgd.crop(cropCoords)
    bkgd = app.loadImage(r"Graphics/winGame.jpg")
    imageWidth, imageHeight = bkgd.size
    imagecx, imagecy = imageWidth//2, imageHeight//2
    cropCoords = imagecx-app.cx, imagecy-app.cy, imagecx+app.cx, imagecy+app.cy
    app.winModeImage =  bkgd.crop(cropCoords)
    
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


def drawHealthBar(app, canvas, character, x0, y0, x1, y1):
    x2, y2, x3, y3 = x0 + app.cellWidth//10, y0 - app.cellWidth//10, x1 - app.cellWidth//10, y0 - app.cellWidth//10*3
    canvas.create_rectangle(x2, y2, x3, y3)
    x4, y4, x5, y5 = x2, y2, character.health/100*(x3-x2)+x2, y3
    canvas.create_rectangle(x4, y4, x5, y5, fill="red")
    
def drawPlayer(app, canvas):
    # draw player sprite
    if app.mode == "mazeMode":
        player = app.mazePlayer
    else: 
        player = app.player
    sprite = app.playerSprites[convertDirections(app, player.dir)][app.playerSpriteCounter]
    x0, y0, x1, y1 = getCellBounds(app, (player.row, player.col) )
    cx, cy = (x0+x1)//2, (y0+y1)//2
    
    sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
    # health bar
    if app.mode != "mazeMode":
        drawHealthBar(app, canvas, app.player, x0, y0, x1, y1)
    
    # # draw basic player
    # drawCell(app, canvas, app.player.row, app.player.col, app.player.color)

# takes in the character and returns the current sprite to be used
def getSpriteInFrame(app, character, sprites, spriteCounter):
    print("here", character.dir)
    sprite = sprites[convertDirections(app, character.dir)][spriteCounter]
    x0, y0, x1, y1 = getCellBounds(app, (character.row, character.col) )
    cx, cy = (x0+x1)//2, (y0+y1)//2
    sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
    return sprite, cx, cy

def drawEnemies(app, canvas):
    # draw sprite
    if app.mode == "roomMode":

        for enemy in app.currRoom.roomEnemies:
            sprite, cx, cy = getSpriteInFrame(app, enemy, 
                            app.enemySprites, app.enemySpriteCounter)
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
            x0, y0, x1, y1 = getCellBounds(app, (enemy.row, enemy.col) )
            drawHealthBar(app, canvas, enemy, x0, y0, x1, y1)
    
    else:
        pass
    # draw basic enemy
    # temporarily having only 1 enemy
    # enemy = app.enemy 
    # drawCell(app, canvas, enemy.row, enemy.col, enemy.color)
    # for enemy in app.roomEnemies:
    #    drawCell(app, canvas, enemy.row, enemy.col, enemy.color)

# draws one cell according to its row and col position
def drawCell(app, canvas, row, col, cellColor):
    x = app.margin + col * app.cellWidth
    y = app.margin + row * app.cellHeight
    canvas.create_oval(x, y, x + app.cellWidth, y + app.cellHeight,
                            fill=cellColor)

#########################################################
# MAZE MODE
#########################################################

def initMazeModeParams(app):
    # init general 
    app.mazePlayer = Player()
    app.mazeGraph = prim(app)
    
    # init enemies in maze
    # app.enemy = Enemy(5,5)
    # app.path = bfs(app.graph, 
    #             (app.enemy.row, app.enemy.col),
    #             (app.player.row, app.player.col))
    
    # init portal
    app.portalSprite = app.loadImage(r"Graphics/portal.png")
    app.portalSprites = createObjectSprites(app, app.portalSprite, 1, 4, 4)
    app.portalSpriteCounter = 0
    app.portal = Portal(random.randint(0, app.rows-1), random.randint(0, app.cols-1))
    


def mazeMode_timerFired(app):
    player = app.mazePlayer
    if len(app.visitedRooms) == app.totalRooms:
        app.completedRooms = True

    if app.completedRooms:
        if app.portal.checkCollision(player):
            print("Going to boss room...")
            app.mode = "bossMode"
            initBossModeParams(app)

    else:
        for door in app.doors:
            if door.checkCollision(player):
                print("Going to a room...")
                app.mode = "roomMode"
                app.currRoomNum = door.roomNum
                app.currRoom = app.rooms[app.currRoomNum]
                app.player.row, app.player.col = (0,0)
        
    
def mazeMode_keyPressed(app, event):
    playerControls(app, event, app.mazePlayer)

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
        line = x0, y0, x0, y0 + app.cellHeight
    elif nodeCol == neighbourCol:
        if nodeRow > neighbourRow: # node is on bottom of neighbour
            x0, y0, x1, y1 = getCellBounds(app, node)
        else:  # neighbour at bottom
            x0, y0, x1, y1 = getCellBounds(app, neighbour)
        line = x0, y0, x0 + app.cellWidth, y0
    canvas.create_line(line)

def drawPortal(app, canvas):
    sprite = app.portalSprites[app.portalSpriteCounter]
    x0, y0, x1, y1 = getCellBounds(app, (app.portal.row, app.portal.col) )
    cx, cy = (x0+x1)//2, (y0+y1)//2
    sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
    # drawCell(app, canvas, app.portal.row, app.portal.col, "purple")

def mazeMode_redrawAll(app, canvas):
    drawGraph(app, canvas, app.mazeGraph)
    drawPlayer(app, canvas)
    drawEnemies(app, canvas)
    # for debugging path-finding of enemy
    # for (row, col) in app.path:
    #        drawCell(app, canvas, row, col, "red")
    for i in range(app.totalRooms):
        drawDoor(app, canvas, i)
    canvas.create_rectangle(app.margin, app.margin, app.gridWidth+app.margin, app.gridHeight+app.margin)
    if app.completedRooms: drawPortal(app, canvas)
    

#########################################################
# ROOM MODE 
#########################################################

def initRoomModeParams(app):
    app.player = Player()
    app.enemyStepTime = 0.3

    # init graphics
    app.wallSprite = app.loadImage(r"Graphics/wall.jpg")
    app.enemySprite = app.loadImage(r"Graphics/big_worm.png")
    app.enemySprites = createMovingSprites(app, app.enemySprite, 4, 3, range(4), 3)
    app.enemySpriteCounter = 0
    app.healthBoosterSprite = app.loadImage(r"Graphics/healthBooster.png")

    # init all rooms
    app.completedRooms = False

    app.totalRooms = 2
    app.rooms = []
    app.currRoom = None
    app.currRoomNum = None
    app.visitedRooms = set()

    app.doorCoords = []
    app.doors = []
    
    for i in range(app.totalRooms):
        row, col = random.randint(0, app.rows-1), random.randint(0, app.cols-1)
        while (row, col) in app.doorCoords:
            row, col = random.randint(0, app.rows-1), random.randint(0, app.cols-1)
        door = Door(row, col, i)
        app.doors.append(door)
        app.doorCoords.append( (row,col) )
        enemyCount = 1
        room = Room(app, i, row, col, enemyCount)
        app.rooms.append(room)

    # The following inits have been done within each instance of room
    # # app.roomItems = []
    # app.walls, app.wallsCoords = createWalls(app)
    # # print("start graph")
    # app.roomGraph = createRoomGraph(app)
    # # print(app.graph.table)
    # # can proceed to add more enemies into list later on 
    # app.enemyCount = 1
    # app.roomEnemies = []
    # for i in range(app.enemyCount):
    #     row, col = createObjectInRoom(app)
    #     app.roomEnemies.append(Enemy(row, col))
    # for enemy in app.roomEnemies:
    #     enemy.path = bfs(app.roomGraph, (enemy.row, enemy.col),
    #         (app.player.row, app.player.col) )

    # row, col = createObjectInRoom(app)
    # app.healthBooster = HealthBooster(row, col)
    # row, col = createObjectInRoom(app)
    # app.timeFreezer = TimeFreezer(row, col)

def roomMode_timerFired(app):
    currTime = time.time()

    # health booster item
    app.currRoom.healthBooster.checkCollision(app.player)

    # freeze time item
    if app.currRoom.timeFreezer.collected:
        if currTime - app.startFreezeTime > 10:
            app.enemyStepTime = 0.3
    if app.currRoom.timeFreezer.checkCollision(app.player): 
        app.startFreezeTime = time.time()
        app.enemyStepTime = 3

    # enemy recalculates path every 5s
    if currTime - app.bfsStartTime > 5:
        for enemy in app.currRoom.roomEnemies:
            enemy.path = bfs(app.currRoom.roomGraph, (enemy.row, enemy.col),
                (app.player.row, app.player.col) )
        app.dfsStartTime = time.time()

    # enemy takes a step every interval of stepTime
    if currTime - app.startTime > app.enemyStepTime:
        for enemy in app.currRoom.roomEnemies:
            if enemy.path != []:
                prevRow, prevCol = enemy.row, enemy.col
                enemy.row, enemy.col = enemy.path.pop()
                enemy.dir = (enemy.row - prevRow, enemy.col - prevCol)
                # print(prevRow, prevCol, enemy.row, enemy.col, enemy.dir)
                # print("moved", enemy.row, enemy.col)
        app.startTime = time.time()

    # check if enemy attacked player
    for enemy in app.currRoom.roomEnemies:
        if enemy.checkCollision(app.player):
            app.player.health -= 10
            if app.player.health < 0: 
                print("GAME OVER!")
                app.mode = "loseMode"

    # check if player attacked enemy
    for bullet in app.player.bullets:
        print("bullet:", bullet)
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol 
        bullet.spriteCounter = (1 + bullet.spriteCounter) % len(app.bulletSprites)
        for enemy in app.currRoom.roomEnemies:
            enemy = bullet.checkCollision(enemy)
            if enemy.health < 0: 
                app.currRoom.roomEnemies.remove(enemy)

    # check if player has killed all enemies
    if app.currRoom.roomEnemies == []:
        if app.currRoom.door.checkCollision(app.player):
            print("Congrats! Going back to maze...")
            app.mode = "mazeMode"

# should add some stuff 
def roomMode_keyPressed(app, event):
    playerControls(app, event, app.player)

#####################################################
# Drawing Functions
#####################################################

# draws one cell according to its row and col position
def drawCell(app, canvas, row, col, cellColor):
    x = app.margin + col * app.cellWidth
    y = app.margin + row * app.cellHeight
    canvas.create_rectangle(x, y, x + app.cellWidth, y + app.cellHeight,
                            fill=cellColor)

# draws every individual cell in the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
                cellColor = app.board[row][col]
                drawCell(app, canvas, row, col, cellColor) 

def drawRoomWalls(app, canvas):
    for wallCoord in app.currRoom.wallsCoords:
        ## draw walls using sprite, need to loop through wall in wall coords
        x0, y0, x1, y1 = getCellBounds(app, wallCoord)
        cx, cy = (x0+x1)//2, (y0+y1)//2
        imageWidth, imageHeight = app.wallSprite.size
        scaleFactor =  (x1-x0) / imageWidth 
        # print(scaleFactor)
        wallSprite = app.scaleImage(app.wallSprite, scaleFactor)
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(wallSprite))

        # draw wall as a circle, loop through wall in walls
        # drawCell(app, canvas, wall.row, wall.col, wall.color)

def drawBullets(app, canvas):
    for bullet in app.player.bullets:
        # sprite = app.bulletSprites[bullet.spriteCounter]
        sprite = app.oneBulletSprite
        x0, y0, x1, y1 = getCellBounds(app, (bullet.row, bullet.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))

    # drawCell(app, canvas, bullet.row, bullet.col, "yellow")

def drawDoor(app, canvas, doorNum=None):
    sprite = app.doorSprite
    x0, y0, x1, y1 = getCellBounds(app, app.doorCoords[doorNum] )
    cx, cy = (x0+x1)//2, (y0+y1)//2
    sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))

def drawHealthBooster(app, canvas):
    if not app.currRoom.healthBooster.collected:
        sprite = app.healthBoosterSprite
        x0, y0, x1, y1 = getCellBounds(app, (app.currRoom.healthBooster.row, app.currRoom.healthBooster.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))

def drawTimeFreezer(app, canvas):
    if not app.currRoom.timeFreezer.collected:
        sprite = app.timeFreezerSprite
        x0, y0, x1, y1 = getCellBounds(app, (app.currRoom.timeFreezer.row, app.currRoom.timeFreezer.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))

def roomMode_redrawAll(app, canvas):
    # drawBoard(app, canvas)
    drawRoomWalls(app, canvas)
    drawPlayer(app, canvas)
    drawEnemies(app, canvas)
    drawBullets(app, canvas)
    drawHealthBooster(app, canvas)
    drawTimeFreezer(app, canvas)

    if app.currRoom.roomEnemies == []: drawDoor(app, canvas, app.currRoomNum)


#########################################################
# BOSS MODE
#########################################################


def initBossModeParams(app):
    app.boss = Boss(10, 10)
    app.player = Player()
    app.gameEvent = None
    app.cols, app.rows, app.margin, app.cellSize = 20, 20, 0, 20
    app.board = [ ["white"] *  app.cols for i in range(app.rows)]
    app.bossSprite = app.loadImage(r"Graphics/man_eater_flower.png")
    app.bossSprites = createMovingSprites(app, app.bossSprite, 4, 3, range(4), 3)
    app.bossSpriteCounter = 0

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
        bullet.checkCollision(app.boss)
    for bullet in app.boss.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol
        bullet.checkCollision(app.player)
    if app.boss.health < 0: app.winGame = True
    if app.player.health < 0: app.winGame = False

    if app.winGame != None:
        if app.winGame: app.mode = "winMode"
        else: app.mode = "loseMode"


def drawBossRoomBullets(app, canvas):
    for bullet in app.player.bullets:
        sprite = app.bulletSprites[bullet.spriteCounter]
        x0, y0, x1, y1 = getCellBounds(app, (bullet.row, bullet.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
    
    for bullet in app.boss.bullets:
        sprite = app.bulletSprites[bullet.spriteCounter]
        x0, y0, x1, y1 = getCellBounds(app, (bullet.row, bullet.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
        canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))

    # for bullet in app.player.bullets:
    #     drawCell(app, canvas, bullet.row, bullet.col, "yellow")

    # for bullet in app.boss.bullets:
    #     drawCell(app, canvas, bullet.row, bullet.col, "yellow")

def drawBoss(app, canvas):
    # static image of boss right now
    sprite = app.bossSprites["Down"][app.bossSpriteCounter]
    x0, y0, x1, y1 = getCellBounds(app, (app.boss.y, app.boss.x) )
    cx, cy = (x0+x1)//2, (y0+y1)//2
    sprite = sprite.resize( (int(x1-x0), int(y1-y0)) )
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(sprite))
    drawHealthBar(app, canvas, app.boss, x0, y0, x1, y1)
    
    # drawCell(app, canvas, app.boss.y, app.boss.x, "green")


def bossMode_redrawAll(app, canvas):
    print(app.gameEvent)
    print(app.boss.x, app.boss.y)
    # drawBoard(app, canvas)
    drawPlayer(app, canvas)
    drawBoss(app, canvas)
    drawBossRoomBullets(app, canvas)


#######################################################
# END GAME
#######################################################

def winMode_redrawAll(app, canvas):
    
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.winModeImage))
    canvas.create_text(app.width//2, app.height//2, text="YOU HAVE ESCAPED!", font="Arial 30", fill="white")

def loseMode_redrawAll(app, canvas):
    
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.loseModeImage))
    canvas.create_text(app.width//2, app.height//2, text="GAME OVER!", font="Arial 30", fill="white")

runApp(width=WIDTH, height=HEIGHT)