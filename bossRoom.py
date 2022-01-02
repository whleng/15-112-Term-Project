import random
from objects import *
from cmu_112_graphics import * 

#########################################################
# bossRoom.py
# This file contains the functions and objects relevant to the boss room
#########################################################

##################################################################
# INIT BOSS
##################################################################

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
        if event == "player moves":
            return attackState()
        return self

class attackState(State):
    def on_event(self, app, event):
        if event == "low health" or event == "player attacks":
            return defendState()
        # shoot at player
        attack(app)
        return self
            
class defendState(State):
    def on_event(self, app, event):    
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
        self.lavas = []

    def on_event(self, app, event):
        # assigns the event to the particular state it is in
        self.state = self.state.on_event(app, event)

def defend(app):
    step = 1
    cornerThresh = 3
    app.boss.shield = True
    for bullet in app.player.bullets:
        if isInRange(app, bullet, app.boss):
            stepDir = random.choice([1,-1])
            if bullet.dir[0] != 0: # (1,0) or (-1,0) horizontal movement
                if app.boss.y > app.rows-cornerThresh:
                    stepDir = -1
                elif app.boss.y < cornerThresh:  
                    stepDir = 1
                app.boss.x += step * stepDir
                if app.boss.x < 0:
                    app.boss.x = 0 
                elif app.boss.x >= app.cols:
                    app.boss.x = app.cols - 1
            elif bullet.dir[1] != 0: # (0,1) or (0,-1) vertical movement
                if app.boss.x > app.cols-cornerThresh:
                    stepDir = -1
                elif app.boss.x < cornerThresh:  
                    stepDir = 1
                app.boss.y += step * stepDir 
                if app.boss.y < 0:
                    app.boss.y = 0 
                elif app.boss.y >= app.rows:
                    app.boss.y = app.rows - 1
            return
    
def isInRange(app, bullet, boss):
    bufferSpace = 3 # cells
    return (bullet.row - bufferSpace < boss.y < bullet.row + bufferSpace
        and bullet.col - bufferSpace < boss.x < bullet.col + bufferSpace)

import math
import time

def attack(app):
    currTime = time.time()
    if currTime - app.bossRoomStartTime > 1:
        # creating bullets that travel in dir of player
        rowDiff = (app.player.row - app.boss.y)
        colDiff = (app.player.col - app.boss.x)
        magnitude = math.sqrt(rowDiff**2 + colDiff**2)
        dir = [ (1/magnitude) * rowDiff, (1/magnitude) * colDiff ]
        bullet = Bullet(app.boss.y, app.boss.x, dir)
        app.boss.bullets.append( bullet )

        # create lava that path finds to player
        if len(app.boss.lavas) < 5:
            lava = Lava(app.boss.y, app.boss.x)
            lava.path = bfs(app.bossGraph, (app.boss.y, app.boss.x),
                (app.player.row, app.player.col) )
            print(lava.path)
            app.boss.lavas.append(lava) 

        app.bossRoomStartTime = time.time()
        

def isLegalMove(app, playerRow, playerCol, prevPlayerRow=None, prevPlayerCol=None):
    return (0 <= playerRow < app.rows and
            0 <= playerCol < app.cols)

def convertDirections(app, dir):
    if dir in app.directions: # in drow, dcol form
        return app.arrowKeys[app.directions.index(dir)]
    elif dir in app.arrowKeys: # in arrow key form
        return app.directions[app.arrowKeys.index(dir)]

###############################################################
# INIT ROOM

def createBossRoomObstacles(app):
    barrelCount = 10
    app.barrelCoords = set()
    app.barrelCoords.add( (0,0) )
    app.barrelCoords.add( (app.boss.y, app.boss.x) )
    app.barrels = list()
    while len(app.barrels) < barrelCount:
        row, col = createObjectInRoom(app, app.barrelCoords)
        barrel = Wall(row, col)
        app.barrels.append(barrel)
        app.barrelCoords.add( (row, col) )
    app.barrelCoords.remove( (0,0) )
    app.barrelCoords.remove( (app.boss.y, app.boss.x) )

  