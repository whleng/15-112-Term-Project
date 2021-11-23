import random

#########################################################
# GENERAL FUNCTIONS
#########################################################

# cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
def getCellBounds(app, node):
    row, col = node
    x0 = app.margin + col * app.cellWidth
    x1 = app.margin + (col+1) * app.cellWidth
    y0 = app.margin + row * app.cellHeight
    y1 = app.margin + (row+1) * app.cellHeight
    return (x0, y0, x1, y1)

# checks whether player's movement is legal
def isLegalMove(app, playerRow, playerCol, prevPlayerRow=None, prevPlayerCol=None):
    if app.mode == "bossMode":
        return (0 <= playerRow < app.rows and 0 <= playerCol < app.cols)
    elif app.mode == "mazeMode":
        return (playerRow, playerCol) in app.mazeGraph.getNeighbours((prevPlayerRow, prevPlayerCol))
    elif app.mode == "roomMode":
        return (playerRow, playerCol) in app.currRoom.roomGraph.getNeighbours((prevPlayerRow, prevPlayerCol))
    
# converts between (drow, dcol) and name of direction
def convertDirections(app, dir):
    print(dir)
    if dir in app.directions: # in drow, dcol form
        return app.arrowKeys[app.directions.index(dir)]
    elif dir in app.arrowKeys: # in arrow key form
        return app.directions[app.arrowKeys.index(dir)]

# player's movements and attack controls
def playerControls(app, event, player):
    app.playerSpriteCounter = (1 + app.playerSpriteCounter) % len(app.playerSprites[convertDirections(app, player.dir)])
    if event.key in app.arrowKeys:
        drow, dcol = convertDirections(app, event.key)
        playerRow = player.row + drow
        playerCol = player.col + dcol
        if isLegalMove(app, playerRow, playerCol, player.row, player.col):
            player.row = playerRow
            player.col = playerCol
            player.dir = (drow, dcol)
    elif event.key == "Space":
        player.attack()

# Referenced from
# http://www.cs.cmu.edu/~112/notes/notes-graphics.html#installingModules
# and Tze Hng Loke (tloke)
# returns a dictionary of sprites with directions based on spritesheet
def createMovingSprites(app, spriteSheet, spriteSheetRows, spriteSheetCols, spriteRows, spriteCols):
    sprites = {'Left': [], 'Right': [], 'Up': [], 'Down': []} 
    imageWidth, imageHeight = spriteSheet.size
    # spriteHeightFactor = app.cellWidth / imageHeight
    dirs = ["Up", "Left", "Down", "Right"]
    for row in range(4): # leftRow, rightRow, upRow, downRow 
        for col in range(spriteSheetCols):
            if col < spriteCols: 
                spriteRow, dir = spriteRows[row], dirs[row]
                sprite = spriteSheet.crop((imageWidth/spriteSheetCols*col, imageHeight/spriteSheetRows*spriteRow, 
                            imageWidth/spriteSheetCols*(col+1) , imageHeight/spriteSheetRows*(spriteRow+1)))
                #scaledsprite = app.scaleImage(sprite, spriteHeightFactor)
                sprites[dir].append(sprite)
    return sprites

# Referenced from
# http://www.cs.cmu.edu/~112/notes/notes-graphics.html#installingModules
# and Tze Hng Loke (tloke)
# returns a dictionary of sprites based on spritesheet
def createObjectSprites(app, spriteSheet, spriteSheetRows, spriteSheetCols, spriteCols):
    sprites = list()
    imageWidth, imageHeight = spriteSheet.size
    # spriteHeightFactor = app.cellWidth / imageHeight
    for row in range(spriteSheetRows):
        for col in range(spriteSheetCols):
            if col < spriteCols: 
                sprite = spriteSheet.crop((imageWidth/spriteSheetCols*col, imageHeight/spriteSheetRows*row, 
                            imageWidth/spriteSheetCols*(col+1) , imageHeight/spriteSheetRows*(row+1)))
                #scaledsprite = app.scaleImage(sprite, spriteHeightFactor)
                sprites.append(sprite)
    return sprites

# returns a (row, col) that is unoccupied
def createObjectInRoom(app, occupiedCoords):
    row, col = None, None
    while True: 
        if isLegalPlacement(app, row, col, occupiedCoords): break
        row, col = random.randint(0, app.rows-1), random.randint(0, app.cols-1)
    return row, col

# check if (row, col) is occupied and within grid
def isLegalPlacement(app, row, col, occupiedCoords):
    return (row != None and col != None and
           0 <= row < app.rows and
           0 <= col < app.cols and
           (row, col) not in occupiedCoords)
