import random
from objects import *
from cmu_112_graphics import * 
# referenced structure from 
# https://dev.to/karn/building-a-simple-state-machine-in-python

class State(object):
    def __init__(self):
        print("Current state: ", repr(self))

    def __repr__(self):
        return self.__class__.__name__
        
    def on_event(self, app, event):
        # do some tasks according to the diff events that could occur at this state
        # set the boss to another state
        pass

class idleState(State):
    def on_event(self, app, event):
        print("idle")
        if event == "player moves":
            return attackState()
        return self

class attackState(State):
    def on_event(self, app, event):
        print("attack")
        if event == "low health" or event == "player attacks":
            return defendState()
        # shoot at player
        attack(app)
        return self
            
class defendState(State):
    def on_event(self, app, event):    
        print("defend")        
        if event == "player stops attack":
            return attackState()
        # move away from player
        defend(app)
        return self

class Boss(object):
    def __init__ (self, maxWidth, maxHeight):
        # randomly generates boss in the room
        self.x = random.randint(0, maxWidth)
        self.y = random.randint(0, maxHeight) 
        self.mass = 50
        # initialises the starting state
        self.state = idleState() 
        self.sheild = False
        self.bullets = []

    def on_event(self, app, event):
        # assigns the event to the particular state it is in
        self.state = self.state.on_event(app, event)

def defend(app):
    # step = 10
    app.boss.shield = True
    for bullet in app.player.bullets:
        if isInRange(app, bullet, app.boss):
            app.boss.x += 1 # step
            app.boss.y += 1 # step
            return
    
def isInRange(app, bullet, boss):
    bufferSpace = 3 # cells
    return (bullet.row - bufferSpace < boss.y < bullet.row + bufferSpace
        and bullet.col - bufferSpace < boss.x < bullet.col + bufferSpace)

def attack(app):
    
    bullet = Bullet(app.boss.y, app.boss.x, app.player.dir)
    app.boss.bullets.append( bullet )

def runGame():
    boss = Boss(10, 10)
    boss.on_event("player moves")
    boss.on_event("player attacks")

# runGame()

def appStarted(app):
    app.boss = Boss(10, 10)
    app.player = Player()
    app.gameEvent = None
    app.cols, app.rows, app.margin, app.cellSize = 20, 20, 0, 20
    app.board = [ ["white"] *  app.cols for i in range(app.rows)]
    

def isLegalMove(app, playerRow, playerCol, prevPlayerRow=None, prevPlayerCol=None):
    return (0 <= playerRow < app.rows and
            0 <= playerCol < app.cols)

def convertDirections(app, dir):
    print(dir)
    if dir in app.directions: # in drow, dcol form
        return app.arrowKeys[app.directions.index(dir)]
    elif dir in app.arrowKeys: # in arrow key form
        return app.directions[app.arrowKeys.index(dir)]

def keyPressed(app, event):
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
    elif event.key == "Space":
        app.player.attack()
        app.gameEvent = "player attacks"
    else:         
        app.gameEvent = "player stops attack"

def timerFired(app):
    app.boss.on_event(app, app.gameEvent)
    for bullet in app.player.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol
    for bullet in app.boss.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol

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
    for wall in app.walls:
        ## draw walls using sprite, need to loop through wall in wall coords
        # x0, y0, x1, y1 = getCellBounds(app, wall)
        # cx, cy = (x0+x1)//2, (y0+y1)//2
        # wallSprite = app.wallSprite.resize( (int(x1-x0), int(y1-y0)) )
        # canvas.create_image(cx, cy, image=ImageTk.PhotoImage(wallSprite))

        # draw wall as a circle, loop through wall in walls
        drawCell(app, canvas, wall.row, wall.col, wall.color)

def drawBullets(app, canvas):
    for bullet in app.player.bullets:
        drawCell(app, canvas, bullet.row, bullet.col, "yellow")

    for bullet in app.boss.bullets:
        drawCell(app, canvas, bullet.row, bullet.col, "yellow")

def drawPlayer(app, canvas):
    drawCell(app, canvas, app.player.row, app.player.col, app.player.color)

def drawBoss(app, canvas):
    drawCell(app, canvas, app.boss.y, app.boss.x, "green")

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawPlayer(app, canvas)
    drawBoss(app, canvas)
    drawBullets(app, canvas)

runApp(width=400, height=400)

###############################################################

# other physics elements for fighting player

# determines the final position of two objects after collision
def collision(a, b):
    totalMomentum = a.mass * a.speed - b.mass * b.speed 
    totalKE = 0.5*a.mass*a.speed**2 + 0.5*b.mass*b.speed**2
    # aFinalSpeed, bFinalSpeed 
    pass

def modifySpeed(playerSpeed, playerDirection, windSpeed):
    pass
