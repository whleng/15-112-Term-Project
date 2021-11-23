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
        # print("idle")
        if event == "player moves":
            return attackState()
        return self

class attackState(State):
    def on_event(self, app, event):
        # print("attack")
        if event == "low health" or event == "player attacks":
            return defendState()
        # shoot at player
        attack(app)
        return self
            
class defendState(State):
    def on_event(self, app, event):    
        # print("defend")        
        if event == "player moves":
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
        self.dir = (0,1)
        self.health = 100
        # initialises the starting state
        self.state = idleState() 
        self.sheild = False
        self.bullets = []

    def on_event(self, app, event):
        # assigns the event to the particular state it is in
        self.state = self.state.on_event(app, event)

def defend(app):
    step = 1
    app.boss.shield = True
    for bullet in app.player.bullets:
        if isInRange(app, bullet, app.boss):
            print(bullet.dir)
            stepDir = random.choice([1,-1])
            if bullet.dir[0] != 0: # (1,0) or (-1,0) horizontal movement
                app.boss.x += step * stepDir
            elif bullet.dir[1] != 0: # (0,1) or (0,-1) vertical movement
                app.boss.y += step * stepDir 
            return
    
def isInRange(app, bullet, boss):
    bufferSpace = 3 # cells
    return (bullet.row - bufferSpace < boss.y < bullet.row + bufferSpace
        and bullet.col - bufferSpace < boss.x < bullet.col + bufferSpace)

import math
import time

def attack(app):
    currTime = time.time()
    if currTime - app.startTime > 1:
        rowDiff = (app.player.row - app.boss.y)
        colDiff = (app.player.col - app.boss.x)
        magnitude = math.sqrt(rowDiff**2 + colDiff**2)
        dir = [ (1/magnitude) * rowDiff, (1/magnitude) * colDiff ]
        bullet = Bullet(app.boss.y, app.boss.x, dir)
        app.boss.bullets.append( bullet )
        app.startTime = time.time()

# def appStarted(app):
#     bossRoomInit(app)

def isLegalMove(app, playerRow, playerCol, prevPlayerRow=None, prevPlayerCol=None):
    return (0 <= playerRow < app.rows and
            0 <= playerCol < app.cols)

def convertDirections(app, dir):
    # print(dir)
    if dir in app.directions: # in drow, dcol form
        return app.arrowKeys[app.directions.index(dir)]
    elif dir in app.arrowKeys: # in arrow key form
        return app.directions[app.arrowKeys.index(dir)]

# def redrawAll(app, canvas):
#     drawBoard(app, canvas)
#     drawPlayer(app, canvas)
#     drawBoss(app, canvas)
#     drawBossRoomBullets(app, canvas)

# runApp(width=400, height=400)

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
