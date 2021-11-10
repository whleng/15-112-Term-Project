from cmu_112_graphics import *
import random
import time

class Player(object):
    def __init__(self):
        self.row, self.col = 0, 0
        self.color = "blue"
        self.health = 100
        self.speed = 10 
        self.xp = 10
        self.items = dict()
        self.bullets = []
        self.dir = None

    def jump(self):
        # skip one box when moving in a particular direction
        pass 

    def attack(self):
        bullet = Bullet(self.row, self.col, self.dir)
        self.bullets.append( bullet )
        # generate bullets in the direction it is facing
        # bullets will keep moving with decreasing velocity 
        # player will recoil when shooting bullets
    
class Bullet(object):
    def __init__(self, row, col, dir):
        self.row, self.col = row, col
        self.dir = dir

    def checkCollision(self, enemyList):
        for enemy in enemyList:
            if self.row == enemy.row and self.col == enemy.col:
                enemyList.remove(enemy)
        return enemyList
        # collision with wall occurs when bullet hits wall 
        pass

class Enemy(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.color = "red"

    def followPlayer(self, playerRow, playerCol):
        if self.row > playerRow: self.row -= 1
        elif self.row < playerRow: self.row += 1
        if self.col > playerCol: self.col -= 1
        elif self.col < playerCol: self.col += 1

    def attackPlayer(self, playerRow, playerCol, app):
        pass
        # app.bullets.append

class Wall(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.color = "brown"

class Item(object):
    def __init__(self, name):
        self.name = name

    def collected(self, player):
        player.items[self.name] = player.items.get(self.name, 0) + 1
        
def appStarted(app):
    app.player = Player()
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.board = [ ["white"] *  app.cols for i in range(app.rows)]
    app.roomEnemies = [ Enemy(5,5), Enemy(8,8) ]
    app.roomItems = []
    app.walls, app.wallsCoords = createWalls()
    app.startTime = time.time()
    app.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    # "Up", "Right", "Down", "Left"

# returns the value of game dimensions
def gameDimensions():
    rows, cols, cellSize, margin = 20, 20, 20, 0 
    # game dimensions can be changed here
    return (rows, cols, cellSize, margin)

def createWalls():
    walls = set()
    wallsCoords = set()
    for _ in range(10):
        wall = Wall(random.randint(0,19), random.randint(0, 19))
        walls.add(wall)
        wallsCoords.add((wall.row, wall.col))
    return walls, wallsCoords

def keyPressed(app, event):
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

def isLegalMove(app, playerRow, playerCol):
    if ((playerRow, playerCol) in app.wallsCoords or
        playerRow < 0 or playerRow >= app.rows or
        playerCol < 0 or playerCol >= app.cols):
        print("hit")
        return False
    else: return True

def timerFired(app):
    currTime = time.time()
    if currTime - app.startTime > 1:
        for enemy in app.roomEnemies:
            enemy.followPlayer(app.player.row, app.player.col)
        app.startTime = time.time()
    for bullet in app.player.bullets:
        drow, dcol = bullet.dir
        bullet.row += drow
        bullet.col += dcol
        app.roomEnemies = bullet.checkCollision(app.roomEnemies)
    
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
    canvas.create_rectangle(x, y, x + app.cellSize, y + app.cellSize,
                            fill=cellColor)

def drawPlayer(app, canvas):
    drawCell(app, canvas, app.player.row, app.player.col, app.player.color)

def drawEnemies(app, canvas):
    for enemy in app.roomEnemies:
        drawCell(app, canvas, enemy.row, enemy.col, enemy.color)

def drawWalls(app, canvas):
    for wall in app.walls:
        drawCell(app, canvas, wall.row, wall.col, wall.color)

def drawBullets(app, canvas):
    for bullet in app.player.bullets:
        drawCell(app, canvas, bullet.row, bullet.col, "yellow")

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawWalls(app, canvas)
    drawPlayer(app, canvas)
    drawBullets(app, canvas)
    drawEnemies(app, canvas)
    
runApp(width=400, height=400)