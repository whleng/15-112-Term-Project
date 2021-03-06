from cmu_112_graphics import *
from graph import *
from room import *
from objects import *
from bossRoom import *
from generalFunctions import *
import time

#########################################################
# main.py
# This file contains all the main functions of the project
# including the animation functions
# Run this file to start the game
#########################################################

WIDTH = 800
HEIGHT = 800

def gameDimensions():
    rows, cols, margin = 15, 15, 20  
    # game dimensions can be changed here
    return (rows, cols, margin)

#########################################################
# MAIN APP
#########################################################

def appStarted(app):
    app.mode = "splashscreenMode" 
    # modes: mazeMode, roomMode, bossMode, splashscreenMode, 
    # winMode, loseMode
    app.winGame = None
    app.mazeChoice = "prim"

    initGeneralParams(app) 
    initSprites(app)
    initBackgrounds(app)

    if app.mode == "splashscreenMode":
        app.splashscreen = loadSplashscreen(app)
        createButtons(app)
        
    elif app.mode == "mazeMode":
        
        initMazeModeParams(app)
        initRoomModeParams(app)

    elif app.mode == "roomMode":
        initRoomModeParams(app)

    elif app.mode == "bossMode":
        app.player = Player()
        initBossModeParams(app)
        
   
    
#########################################################
# SPLASHSCREEN MODE
#########################################################

def loadSplashscreen(app):
    bkgd = app.loadImage(r"Graphics/dungeon.jpg")
    imageWidth, imageHeight = bkgd.size
    imagecx, imagecy = imageWidth//2, imageHeight//2
    cropCoords = imagecx-app.cx, imagecy-app.cy, imagecx+app.cx, imagecy+app.cy
    return bkgd.crop(cropCoords)

def drawSplashscreen(app, canvas):
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.splashscreen))

def createButtons(app):
    cx, cy = app.cx, app.cy * 2/3
    width, height = app.width/5, app.height/15
    app.startButton = cx-width, cy-height, cx+width, cy+height

def drawButtons(app, canvas):
    # start button
    cx, cy = app.cx, app.cy * 2/3
    canvas.create_rectangle(app.startButton, fill="brown")
    canvas.create_text(cx, cy, text="Start Game", font="{Century Schoolbook}", fill="white")
    
def splashscreenMode_mousePressed(app, event):
    x0, y0, x1, y1 = app.startButton
    if x0 < event.x < x1 and y0 < event.y < y1:
        initMazeModeParams(app)
        initRoomModeParams(app)
        app.mode = "mazeMode"

def splashscreenMode_keyPressed(app, event):
    if event.key == "k":
        app.mazeChoice = "kruskal"

def splashscreenMode_redrawAll(app, canvas):
    drawSplashscreen(app, canvas)
    drawButtons(app, canvas)


#########################################################
# GENERAL FUNCTIONS (mainly graphics)
#########################################################

def initGeneralParams(app):
    app.cx, app.cy = app.width//2, app.height//2
    app.timerDelay = 200
    
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


def initBackgrounds(app):
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

    app.mazeBkgd = createBackground(app, app.loadImage(r"Graphics/dungeon floor.jpg"))
    app.roomBkgd = createBackground(app, app.loadImage(r"Graphics/roomBackground.jpg"))

def createBackground(app, image):
    imageWidth, imageHeight = image.size
    imagecx, imagecy = imageWidth//2, imageHeight//2
    if imageWidth/imageHeight < app.width/app.height: 
        # crop to width
        image = image.resize( (int(app.width), int(app.width/imageWidth * imageHeight)) )
    else:        
        # crop to height
        image = image.resize( ( int(app.height/imageHeight * imageWidth), int(app.height)) )
    imageWidth, imageHeight = image.size
    imagecx, imagecy = imageWidth//2, imageHeight//2
    cropCoords = imagecx-app.cx, imagecy-app.cy, imagecx+app.cx, imagecy+app.cy    
    return ImageTk.PhotoImage(image.crop(cropCoords))

def initSprites(app):
    app.playerSpriteSheet = app.loadImage(r"Graphics/player.png")
    app.playerSprites = createMovingSprites(app, app.playerSpriteSheet, 
                    21, 13, range(8,12), 9)
    app.playerSpriteCounter = 0
    
    app.oneBulletSprites = createBulletSprites(app, "Graphics/oneBullet.png")
    
    app.wallSprite = processSprite(app, "Graphics/wall.jpg")
    
    app.enemySprite = app.loadImage(r"Graphics/big_worm.png")
    app.enemySprites = createMovingSprites(app, app.enemySprite, 4, 3, range(4), 3)
    app.enemySpriteCounter = 0

    app.ghostSprite = app.loadImage(r"Graphics/ghost.png")
    app.ghostSprites = createMovingSprites(app, app.ghostSprite, 4, 3, range(4), 3)

    app.eyeballSprite = app.loadImage(r"Graphics/eyeball.png")
    app.eyeballSprites = createMovingSprites(app, app.eyeballSprite, 4, 3, range(4), 3)

    app.batSprite = app.loadImage(r"Graphics/bat.png")
    app.batSprites = createMovingSprites(app, app.batSprite, 4, 3, range(4), 3)

    app.slimeSprite = app.loadImage(r"Graphics/slime.png")
    app.slimeSprites = createMovingSprites(app, app.slimeSprite, 4, 3, range(4), 3)

    app.doorSprite = processSprite(app, "Graphics/door.png")
    app.openedDoorSprite =  processSprite(app, "Graphics/openDoor.png")
   
    app.healthBoosterSprite = processSprite(app, "Graphics/healthBooster.png")
    app.timeFreezerSprite = processSprite(app, "Graphics/hourglass.png")

    app.portalSprite = app.loadImage(r"Graphics/portal.png")
    app.portalSprites = createObjectSprites(app, app.portalSprite, 1, 4, 4)
    app.portalSpriteCounter = 0

    app.bossSprite = app.loadImage(r"Graphics/man_eater_flower.png")
    app.bossSprites = createMovingBossSprites(app, app.bossSprite, 4, 3, range(4), 3)
    app.bossSpriteCounter = 0

    app.barrelSprite = processSprite(app, "Graphics/barrel.png")

    app.lavaSprite = processSprite(app, "Graphics/lava.png")
    app.invisibilityPotionSprite = processSprite(app, "Graphics/blue potion.png")


def createBulletSprites(app, path):
    sprite = app.loadImage(path)
    _, imageHeight = sprite.size
    spriteHeightFactor = app.cellHeight / imageHeight
    sprite = app.scaleImage(sprite, spriteHeightFactor)
    sprites = {'Left': [], 'Right': [], 'Up': [], 'Down': []} 
    sprites["Right"] = ImageTk.PhotoImage(sprite)
    # down       
    newSprite = sprite.rotate(-90)
    sprites["Down"] = ImageTk.PhotoImage(newSprite)
    # up       
    newSprite = sprite.rotate(90)
    sprites["Up"] = ImageTk.PhotoImage(newSprite)
    # left       
    newSprite = sprite.rotate(180)
    sprites["Left"] = ImageTk.PhotoImage(newSprite)
    return sprites

def createMovingBossSprites(app, spriteSheet, spriteSheetRows, spriteSheetCols, spriteRows, spriteCols):
    sprites = {'Left': [], 'Right': [], 'Up': [], 'Down': []} 
    imageWidth, imageHeight = spriteSheet.size
    spriteHeightFactor = app.cellHeight / (imageHeight/(spriteSheetRows+1))
    dirs = ["Up", "Left", "Down", "Right"]
    for row in range(4): # leftRow, rightRow, upRow, downRow 
        for col in range(spriteSheetCols):
            if col < spriteCols: 
                spriteRow, dir = spriteRows[row], dirs[row]
                sprite = spriteSheet.crop((imageWidth/spriteSheetCols*col, imageHeight/spriteSheetRows*spriteRow, 
                            imageWidth/spriteSheetCols*(col+1) , imageHeight/spriteSheetRows*(spriteRow+1)))
                scaledsprite = app.scaleImage(sprite, spriteHeightFactor*3)
                sprites[dir].append(ImageTk.PhotoImage(scaledsprite))
    return sprites

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
    canvas.create_image(cx, cy, image=sprite)
    # health bar
    drawHealthBar(app, canvas, player, x0, y0, x1, y1)
    
def drawEnemies(app, canvas):
    # draw sprite
    if app.mode == "mazeMode":
        enemyList = app.mazeEnemies
        sprites = app.ghostSprites 
    elif app.mode == "roomMode":
        enemyList = app.currRoom.roomEnemies
        if app.currRoom.roomNum == 1:
            sprites = app.enemySprites
        elif app.currRoom.roomNum == 2:
            sprites = app.batSprites
        elif app.currRoom.roomNum == 3: 
            sprites = app.slimeSprites
        else: 
            sprites = app.eyeballSprites
    for enemy in enemyList:
        sprite, cx, cy = getSpriteInFrame(app, enemy, 
                        sprites, app.enemySpriteCounter)
        canvas.create_image(cx, cy, image=sprite)
        x0, y0, x1, y1 = getCellBounds(app, (enemy.row, enemy.col) )
    if app.mode != "mazeMode":
        for enemy in enemyList:
            x0, y0, x1, y1 = getCellBounds(app, (enemy.row, enemy.col) )
            drawHealthBar(app, canvas, enemy, x0, y0, x1, y1)

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
    if app.mazeChoice == "prim":
        app.mazeGraph = prim(app)
    elif app.mazeChoice == "kruskal":
        app.mazeGraph, _ = kruskal(app, "maze")
    app.mazeGraph = removeDeadEnds(app, app.mazeGraph)
    app.mazeAllNodes = createAllNodes(app)
    enemyCount = 3
    # init enemies in maze
    app.mazeEnemies = []
    for _ in range(enemyCount):
        row, col = random.randint(5, app.rows-1), random.randint(5, app.cols-1)
        app.mazeEnemies.append( Enemy(row, col) )
    for enemy in app.mazeEnemies:
        enemy.path = []
    # init portal
    app.portal = Portal(random.randint(5, app.rows-1), random.randint(5, app.cols-1))
    # init lava traps
    lavaCount = 5
    app.mazeLavas = []
    for _ in range(lavaCount):
        row, col = random.randint(5, app.rows-1), random.randint(5, app.cols-1)
        app.mazeLavas.append( Lava(row, col) )
    # init health potion
    row, col = random.randint(5, app.rows-1), random.randint(5, app.cols-1)
    app.mazeHealthBooster = HealthBooster(row, col)

def mazeMode_timerFired(app):
    player = app.mazePlayer
    currTime = time.time()

    # health item
    app.mazePlayer = app.mazeHealthBooster.checkCollision(app.mazePlayer)

    # lava
    for lava in app.mazeLavas:
        # modifies player's health 
        app.mazePlayer = lava.checkCollision(app.mazePlayer, app.mazeLavas)
        if app.mazePlayer.health < 0:
            app.mode = "loseMode"

    # enemy code
    # enemy recalculates path every 3s
    targetRow, targetCol = app.mazePlayer.row, app.mazePlayer.col

    # vary path finding algorithm for different enemies
    if currTime - app.bfsStartTime > 3:
        for enemy in app.mazeEnemies:
            if app.mazeEnemies.index(enemy) % 2 == 0:
                enemy.path = dijkstra(app.mazeGraph, (enemy.row, enemy.col), 
                            (targetRow, targetCol), app.mazeAllNodes)
            else:
                enemy.path = bfs(app.mazeGraph, (enemy.row, enemy.col), 
                         (targetRow, targetCol) )
            app.dfsStartTime = time.time()

    # enemy takes a step every interval of stepTime
    if currTime - app.startTime > 0.4:
        for enemy in app.mazeEnemies:
            if enemy.path != []:
                prevRow, prevCol = enemy.row, enemy.col
                enemy.row, enemy.col = enemy.path.pop()
                enemy.dir = (enemy.row - prevRow, enemy.col - prevCol)
                if enemy.checkCollision(app.mazePlayer): 
                    app.mazePlayer.health -= 10
                    if app.mazePlayer.health < 0:
                        app.mode = "loseMode"
        app.startTime = time.time()

    # check completion of rooms 

    if len(app.visitedRooms) == app.totalRooms:
        app.completedRooms = True

    if app.completedRooms:
        if app.portal.checkCollision(player):
            print("Going to boss room...")
            app.mode = "bossMode"
            initBossModeParams(app)

    else:
        for door in app.doors:
            if door.checkCollision(player) and door.roomNum not in app.visitedRooms:
                print("Going to a room...")
                app.mode = "roomMode"
                app.currRoomNum = door.roomNum
                app.currRoom = app.rooms[app.currRoomNum]
                app.player.row, app.player.col = (0,0)
                app.player.health = app.mazePlayer.health
                app.player.bullets = []
                app.visitedRooms.add(door.roomNum)
        
    
def mazeMode_keyPressed(app, event):
    playerControls(app, event, app.mazePlayer)
    if event.key == "b":
        initBossModeParams(app)
        app.mode = "bossMode"

# draw grid based on graph
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
        for neighbour in neighbours:
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
    canvas.create_line(line, width=2)

def drawPortal(app, canvas):
    sprite = app.portalSprites[app.portalSpriteCounter]
    x0, y0, x1, y1 = getCellBounds(app, (app.portal.row, app.portal.col) )
    cx, cy = (x0+x1)//2, (y0+y1)//2
    canvas.create_image(cx, cy, image=sprite)

def drawMazeBkgd(app, canvas):
    canvas.create_image(app.cx, app.cy, image=app.mazeBkgd)

def drawMazeLavas(app, canvas):
    for lava in app.mazeLavas:
        sprite = app.lavaSprite
        x0, y0, x1, y1 = getCellBounds(app, (lava.row, lava.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        canvas.create_image(cx, cy, image=sprite)

def mazeMode_redrawAll(app, canvas):
    drawMazeBkgd(app, canvas)
    drawGraph(app, canvas, app.mazeGraph)
    drawMazeLavas(app, canvas)
    for i in range(app.totalRooms):
        drawDoor(app, canvas, i)
    drawHealthBooster(app, canvas)
    # draw map border
    canvas.create_rectangle(app.margin, app.margin, app.gridWidth+app.margin, 
                    app.gridHeight+app.margin, width=2)
    if app.completedRooms: 
        drawPortal(app, canvas)
    drawPlayer(app, canvas)
    drawEnemies(app, canvas)

#########################################################
# ROOM MODE 
#########################################################

def initRoomModeParams(app):
    app.player = Player()
    
    # init all rooms
    app.completedRooms = False

    app.totalRooms = 4
    app.rooms = []
    app.currRoom = None
    app.currRoomNum = None
    app.visitedRooms = set()

    app.doorCoords = []
    app.doors = []
    
    for i in range(app.totalRooms):
        row, col = random.randint(5, app.rows-1), random.randint(5, app.cols-1)
        while (row, col) in app.doorCoords:
            row, col = random.randint(5, app.rows-1), random.randint(5, app.cols-1)
        door = Door(row, col, i)
        app.doors.append(door)
        app.doorCoords.append( (row,col) )
        enemyCount = i + 1
        room = Room(app, i, row, col, enemyCount)
        app.rooms.append(room)

def roomMode_timerFired(app):
    currTime = time.time()

    # invisible item
    app.currRoom.invisibilityPotion.checkCollision(app.player)
    
    # health booster item
    app.player = app.currRoom.healthBooster.checkCollision(app.player)

    # freeze time item
    if app.currRoom.timeFreezer.collected:
        if currTime - app.startFreezeTime > 10:
            app.currRoom.enemyStepTime = 0.3
    if app.currRoom.timeFreezer.checkCollision(app.player): 
        app.startFreezeTime = time.time()
        app.currRoom.enemyStepTime = 3

    # enemy recalculates path every 3s
    for enemy in app.currRoom.roomEnemies:
        targetRow, targetCol = app.player.row, app.player.col

        # if invisible item collected, enemies keep player's last known position
        if (app.currRoom.invisibilityPotion.collected and 
            (currTime - app.currRoom.invisibilityPotion.collectedTime) < 10):
            if app.currRoom.invisibilityPotion.used == False:
                (row, col) = createObjectInRoom(app, app.currRoom.occupiedCoords)
                app.tempPlayerRow, app.tempPlayerCol = (row, col)
                app.currRoom.invisibilityPotion.used = True
            targetRow, targetCol = app.tempPlayerRow, app.tempPlayerCol
        if currTime - app.bfsStartTime > 3:
            if app.currRoom.roomEnemies.index(enemy) % 2 == 0:
                enemy.path = aStar(app.currRoom.roomGraph, (enemy.row, enemy.col), 
                         (targetRow, targetCol), app.currRoom.roomAllNodes)
            else:
                enemy.path = bfs(app.currRoom.roomGraph, (enemy.row, enemy.col), 
                         (targetRow, targetCol) )
            app.dfsStartTime = time.time()

    # enemy takes a step every interval of stepTime
    if currTime - app.startTime > app.currRoom.enemyStepTime:
        for enemy in app.currRoom.roomEnemies:
            if enemy.path != []:
                prevRow, prevCol = enemy.row, enemy.col
                enemy.row, enemy.col = enemy.path.pop()
                enemy.dir = (enemy.row - prevRow, enemy.col - prevCol)
        app.startTime = time.time()

    # check if enemy attacked player
    for enemy in app.currRoom.roomEnemies:
        if enemy.checkCollision(app.player):
            app.player.health -= 10
            if app.player.health < 0: 
                app.mode = "loseMode"

    # check if player attacked enemy
    for bullet in app.player.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol 
        if (bullet.row < 0 or bullet.row >= app.rows or
            bullet.col < 0 or bullet.col >= app.cols):
            app.player.bullets.remove(bullet) 
        for enemy in app.currRoom.roomEnemies:
            enemy = bullet.checkCollision(enemy)
            if enemy.health < 0: 
                app.currRoom.roomEnemies.remove(enemy)

    # check if player has killed all enemies
    if app.currRoom.roomEnemies == []:
        if app.currRoom.door.checkCollision(app.player):
            print("Congrats! Going back to maze...")
            app.mode = "mazeMode"
            app.mazePlayer.health = app.player.health

def roomMode_keyPressed(app, event):
    playerControls(app, event, app.player)
    if event.key == "b":
        initBossModeParams(app)
        app.mode = "bossMode"

#####################################################
# Drawing Functions
#####################################################

# draws every individual cell in the board
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
                cellColor = app.board[row][col]
                drawCell(app, canvas, row, col, cellColor) 

# draw walls using sprite
def drawRoomWalls(app, canvas):
    for wallCoord in app.currRoom.wallsCoords:
        x0, y0, x1, y1 = getCellBounds(app, wallCoord)
        cx, cy = (x0+x1)//2, (y0+y1)//2
        canvas.create_image(cx, cy, image=app.wallSprite)

def drawBullets(app, canvas):
    for bullet in app.player.bullets:
        sprites = app.oneBulletSprites
        x0, y0, x1, y1 = getCellBounds(app, (bullet.row, bullet.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        if bullet.dir == (1,0): # down
            bulletDir = "Down"
        elif bullet.dir == (-1,0): # up
            bulletDir = "Up"
        elif bullet.dir == (0,-1): # left
            bulletDir = "Left"
        else:
            bulletDir = "Right"
        canvas.create_image(cx, cy, image=sprites[bulletDir])


def drawDoor(app, canvas, doorNum=None):
    sprite = app.openedDoorSprite
    
    if app.mode == "roomMode":
        x0, y0, x1, y1 = getCellBounds(app, (app.currRoom.door.row, app.currRoom.door.col) )
       
    if app.mode == "mazeMode":
        x0, y0, x1, y1 = getCellBounds(app, app.doorCoords[doorNum] )
        if doorNum in app.visitedRooms:
            sprite = app.doorSprite
    
    cx, cy = (x0+x1)//2, (y0+y1)//2
    canvas.create_image(cx, cy, image=sprite)

def drawHealthBooster(app, canvas):
    if app.mode == "roomMode":
        if not app.currRoom.healthBooster.collected:
            sprite = app.healthBoosterSprite
            x0, y0, x1, y1 = getCellBounds(app, (app.currRoom.healthBooster.row, app.currRoom.healthBooster.col) )
            cx, cy = (x0+x1)//2, (y0+y1)//2
            canvas.create_image(cx, cy, image=sprite)
    elif app.mode == "mazeMode":
        if not app.mazeHealthBooster.collected:
            sprite = app.healthBoosterSprite
            x0, y0, x1, y1 = getCellBounds(app, (app.mazeHealthBooster.row, app.mazeHealthBooster.col) )
            cx, cy = (x0+x1)//2, (y0+y1)//2
            canvas.create_image(cx, cy, image=sprite)

def drawTimeFreezer(app, canvas):
    if not app.currRoom.timeFreezer.collected:
        sprite = app.timeFreezerSprite
        x0, y0, x1, y1 = getCellBounds(app, (app.currRoom.timeFreezer.row, app.currRoom.timeFreezer.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        canvas.create_image(cx, cy, image=sprite)


def drawItem(app, canvas, item, sprite):
    if not item.collected:
        x0, y0, x1, y1 = getCellBounds(app, (item.row, item.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        canvas.create_image(cx, cy, image=sprite)


def drawRoomBkgd(app, canvas):
    canvas.create_image(app.cx, app.cy, image=app.roomBkgd)

def roomMode_redrawAll(app, canvas):
    drawRoomBkgd(app, canvas)
    drawRoomWalls(app, canvas)
    drawPlayer(app, canvas)
    drawEnemies(app, canvas)
    drawBullets(app, canvas)
    drawHealthBooster(app, canvas)
    drawTimeFreezer(app, canvas)
    drawItem(app, canvas, app.currRoom.invisibilityPotion, app.invisibilityPotionSprite)

    if app.currRoom.roomEnemies == []: drawDoor(app, canvas)


#########################################################
# BOSS MODE
#########################################################

def initBossModeParams(app):
    app.boss = Boss(10, 10)
    app.player.row, app.player.col = (0,0)
    app.gameEvent = None
    createBossRoomObstacles(app)
    app.bossGraph = createRoomGraph(app, app.barrelCoords)
    app.bossRoomStartTime = time.time()

# assigns the event to boss based on the user interaction
def bossMode_keyPressed(app, event):
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

    # check if player's bullets hit boss
    for bullet in app.player.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol
        bullet.checkCollision(app.boss)
    
    # check if boss' bullets hit player
    for bullet in app.boss.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol
        bullet.checkCollision(app.player)

    currTime = time.time()
    # lava takes a step every interval of stepTime
    print(app.boss.lavas)
    for lava in app.boss.lavas:
        if (currTime - lava.createdTime > 8):
            app.boss.lavas.remove(lava)
        elif (currTime - lava.createdTime > 5 or
            lava.path == []):
            lava.path = []
            lava.checkCollision(app.player, app.boss.lavas)
        else:
            if (currTime - lava.stepTime > 0.3): 
                prevRow, prevCol = lava.row, lava.col
                lava.row, lava.col = lava.path.pop()
                lava.dir = (lava.row - prevRow, lava.col - prevCol)
                lava.checkCollision(app.player, app.boss.lavas)
                lava.stepTime = time.time()

    # check if alive
    if app.boss.health < 0: app.winGame = True
    if app.player.health < 0: app.winGame = False

    # changing mode to end game
    if app.winGame != None:
        if app.winGame: app.mode = "winMode"
        else: app.mode = "loseMode"


def drawBossRoomBullets(app, canvas):
    for bullet in app.player.bullets:
        sprites = app.oneBulletSprites
        x0, y0, x1, y1 = getCellBounds(app, (bullet.row, bullet.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        # default: travelling right
        if bullet.dir == (1,0): # down
            bulletDir = "Down"
        elif bullet.dir == (-1,0): # up
            bulletDir = "Up"
        elif bullet.dir == (0,-1): # left
            bulletDir = "Left"
        else:
            bulletDir = "Right"
        canvas.create_image(cx, cy, image=sprites[bulletDir])
    
    for bullet in app.boss.bullets:
        sprites = app.oneBulletSprites
        x0, y0, x1, y1 = getCellBounds(app, (bullet.row, bullet.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        # default: travelling right
        if bullet.dir == (1,0): # down
            bulletDir = "Down"
        elif bullet.dir == (-1,0): # up
            bulletDir = "Up"
        elif bullet.dir == (0,-1): # left
            bulletDir = "Left"
        else:
            bulletDir = "Right"
        canvas.create_image(cx, cy, image=sprites[bulletDir])

    for lava in app.boss.lavas:
        sprite = app.lavaSprite
        x0, y0, x1, y1 = getCellBounds(app, (lava.row, lava.col) )
        cx, cy = (x0+x1)//2, (y0+y1)//2
        canvas.create_image(cx, cy, image=sprite)

def drawBoss(app, canvas):
    # static image of boss 
    scale = 3 
    sprite = app.bossSprites["Down"][app.bossSpriteCounter]
    x0, y0, x1, y1 = getCellBounds(app, (app.boss.y, app.boss.x) )
    cx, cy = (x0+x1)//2, (y0+y1)//2
    canvas.create_image(cx, cy, image=sprite)
    x0, y0, x1, y1 = getCellBounds(app, (app.boss.y-1, app.boss.x) )

    drawHealthBar(app, canvas, app.boss, x0, y0, x1, y1)
    
def drawObstacles(app, canvas):
    for barrelCoord in app.barrelCoords:
        x0, y0, x1, y1 = getCellBounds(app, barrelCoord)
        cx, cy = (x0+x1)//2, (y0+y1)//2
        canvas.create_image(cx, cy, image=app.barrelSprite)
    

def bossMode_redrawAll(app, canvas):
    drawMazeBkgd(app, canvas)
    print(app.gameEvent)
    drawObstacles(app, canvas)
    drawPlayer(app, canvas)
    drawBossRoomBullets(app, canvas)
    drawBoss(app, canvas)


#######################################################
# END GAME
#######################################################

def winMode_redrawAll(app, canvas):
    
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.winModeImage))
    canvas.create_text(app.width//2, app.height//2, text="YOU HAVE ESCAPED!", font="Arial 30", fill="white")

def winMode_keyPressed(app, event):
    if event.key == "r":
        app.mode = "splashScreenMode"
        appStarted(app)

def loseMode_redrawAll(app, canvas):
    
    canvas.create_image(app.cx, app.cy, image=ImageTk.PhotoImage(app.loseModeImage))
    canvas.create_text(app.width//2, app.height//2, text="GAME OVER!", font="Arial 30", fill="white")


def loseMode_keyPressed(app, event):
    if event.key == "r":
        app.mode = "splashScreenMode"
        appStarted(app)

runApp(width=WIDTH, height=HEIGHT)