from graph import *
from generalFunctions import *
import time


################################################################
# Character Objects
################################################################

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
        pass 

    # generate bullets in self.dir
    def attack(self):
        bullet = Bullet(self.row, self.col, self.dir)
        self.bullets.append(bullet)

class Enemy(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.dir = (0,1)
        self.health = 100
        self.color = "red"
        self.path = []
        self.spriteSheet = []

    # # previous basic follow player code 
    # def followPlayer(self, playerRow, playerCol):
    #     if self.row > playerRow: self.row -= 1
    #     elif self.row < playerRow: self.row += 1
    #     if self.col > playerCol: self.col -= 1
    #     elif self.col < playerCol: self.col += 1

    def checkCollision(self, target):
        if self.row == target.row and self.col == target.col:
            return True

 
################################################################
# Weapons / Attack Items
################################################################

class Bullet(object):
    def __init__(self, row, col, dir):
        self.row, self.col = row, col
        self.dir = dir
        self.spriteCounter = 0
        self.spriteSheet = []

    def checkCollision(self, target):
        loss = 10 #
        try:
            if self.row == target.row and self.col == target.col:
                target.health -= loss
                print(target.health)
        except: # boss
            if (target.y - 1 < self.row < target.y + 1 and 
                target.x - 1 < self.col < target.x + 1):
                target.health -= loss
                print(target.health)
        return target

# lava will be generated from the boss, 
# path path finds itself to player
# lava disappears after 5s
# player dies if it touches lava
class Lava(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.path = []
        self.createdTime = time.time()
        self.stepTime = time.time()
    
    def checkCollision(self, target, lavaList):
        loss = 20 #
        if self.row == target.row and self.col == target.col:
            target.health -= loss
            # print(target.health)
            lavaList.remove(self)
        return target


################################################################
# Static Room Objects
################################################################

class Wall(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.color = "brown"
        self.spriteSheet = []

    def __hash__(self):
        return hash( (self.row, self.col) )

    def __repr__(self):
        return str( (self. row, self.col) )

class Portal(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
    
    def checkCollision(self, target):
        if self.row == target.row and self.col == target.col:
            return True

class Door(object):
    def __init__(self, row, col, roomNum):
        self.row, self.col = row, col
        self.roomNum = roomNum
        self.spriteSheet = []

    def checkCollision(self, target):
        if self.row == target.row and self.col == target.col:
            return True


################################################################
# Collectable Room Objects
################################################################

class HealthBooster(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.collected = False

    def checkCollision(self, target):
        gain = 50
        if (self.row == target.row and self.col == target.col 
            and self.collected == False):
            target.health += gain
            if target.health > 100: target.health = 100
            self.collected = True
            print("HEALTH!")
        return target

class TimeFreezer(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.collected = False

    def checkCollision(self, target):
        if (self.row == target.row and self.col == target.col 
            and self.collected == False):
            self.collected = True
            return True
        return False
 

class InvisibilityPotion(object):
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.collected = False
        self.collectedTime = time.time()
        self.used = False

    def checkCollision(self, target):
        if (self.row == target.row and self.col == target.col 
            and self.collected == False):
            self.collected = True
            return True
        return False

# combat items for boss fight
class Item(object):
    def __init__(self, name, row, col):
        self.name = name
        self.row, self.col = row, col

    def collected(self, player):
        player.items[self.name] = player.items.get(self.name, 0) + 1
