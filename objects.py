from room import *
from graph import *
from generalFunctions import *
from cmu_112_graphics import *


class Sprite(object):
    def __init__(self, character, spriteSheet):
        self.character = character # e.g. app.player
        self.spriteSheet = spriteSheet
#        self.imageWidth, self.imageHeight = spriteSheet.size()

class Player(object):
    def __init__(self, health=100, items=dict()):
        self.row, self.col = 0, 0
        self.color = "blue"
        self.health = health
        self.speed = 10 
        self.xp = 10
        self.items = items
        self.bullets = []
        self.dir = (0,1)
        self.spriteSheet = []

    def jump(self):
        # skip one box when moving in a particular direction
        pass 

    def attack(self):
        bullet = Bullet(self.row, self.col, self.dir)
        self.bullets.append( bullet )
        # generate bullets in the direction it is facing
        # bullets will keep moving with decreasing velocity 
        # player will recoil when shooting bullets
    
class Item(object):
    def __init__(self, row, col):
        self.row, self.col = row, col

    def activate(self, player):
        pass

class Bullet(object):
    def __init__(self, row, col, dir):
        self.row, self.col = row, col
        self.dir = dir
        self.spriteCounter = 0
        self.spriteSheet = []

    def checkCollision(self, target):
        loss = 10
        try:
            if self.row == target.row and self.col == target.col:
                target.health -= loss
                print(target.health)
        except:
            if self.row == target.y and self.col == target.x:
                target.health -= loss
                print(target.health)
        return target

class Enemy(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.dir = (0,1)
        self.health = 100
        self.color = "red"
        self.path = []
        self.spriteSheet = []

    def followPlayer(self, playerRow, playerCol):
        if self.row > playerRow: self.row -= 1
        elif self.row < playerRow: self.row += 1
        if self.col > playerCol: self.col -= 1
        elif self.col < playerCol: self.col += 1

    def attackPlayer(self, playerRow, playerCol, app):
        pass
        # app.bullets.append
    
    def checkCollision(self, target):
        if self.row == target.row and self.col == target.col and self.collected == False:
            return True

class Wall(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.color = "brown"
        self.spriteSheet = []

    def __hash__(self):
        return hash( (self.row, self.col) )

    def __repr__(self):
        return str( (self. row, self.col) )

class Item(object):
    def __init__(self, name):
        self.name = name

    def collected(self, player):
        player.items[self.name] = player.items.get(self.name, 0) + 1

class Portal(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
    
    def checkCollision(self, target):
        if self.row == target.row and self.col == target.col and self.collected == False:
            return True

class Door(object):
    def __init__(self, row, col, doorNum):
        self.row, self.col = row, col
        self.room = doorNum
        self.spriteSheet = []

    def checkCollision(self, target):
        if self.row == target.row and self.col == target.col and self.collected == False:
            return True

class HealthBooster(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.collected = False

    def checkCollision(self, target):
        gain = 10
        if self.row == target.row and self.col == target.col and self.collected == False:
            target.health += gain
            self.collected = True
            print("HEALTH!")
        return target

class TimeFreezer(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.collected = False

    def checkCollision(self, target):
        gain = 10
        if self.row == target.row and self.col == target.col and self.collected == False:
            self.collected = True
            return True
        return False
 
class Room(object):
    def __init__(self, app, roomNum, row, col, enemyCount):
        self.roomNum = roomNum
        self.row, self.col = row, col # position in maze

        self.walls, self.wallsCoords = createWalls(app)
        self.roomGraph = createRoomGraph(app)

        self.roomEnemies = []
        for i in range(enemyCount):
            row, col = createObjectInRoom(app)
        self.roomEnemies.append(Enemy(row, col))
        for enemy in self.roomEnemies:
            enemy.path = bfs(self.roomGraph, (enemy.row, enemy.col),
                (app.player.row, app.player.col) )

        row, col = createObjectInRoom(app)
        self.healthBooster = HealthBooster(row, col)
        row, col = createObjectInRoom(app)
        self.timeFreezer = TimeFreezer(row, col)

        row, col = createObjectInRoom(app)
        self.door = Door(row, col) # to escape back 
