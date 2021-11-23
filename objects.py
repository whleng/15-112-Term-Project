class Sprite(object):
    def __init__(self, character, spriteSheet):
        self.character = character # e.g. app.player
        self.spriteSheet = spriteSheet
#        self.imageWidth, self.imageHeight = spriteSheet.size()

class Player(object):
    def __init__(self):
        self.row, self.col = 0, 0
        self.color = "blue"
        self.health = 100
        self.speed = 10 
        self.xp = 10
        self.items = dict()
        self.bullets = []
        self.dir = (0,1)

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

    def checkCollision(self, target):
        loss = 10
        if self.row == target.row and self.col == target.col:
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
    
class Door(object):
    def __init__(self, row, col):
        self.row, self.col = row, col

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