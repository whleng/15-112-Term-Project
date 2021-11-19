import random

# referenced structure from 
# https://dev.to/karn/building-a-simple-state-machine-in-python

class State(object):
    def __init__(self):
        print("Current state: ", repr(self))

    def __repr__(self):
        return self.__class__.__name__
        
    def on_event(self, event):
        # do some tasks according to the diff events that could occur at this state
        # set the boss to another state
        pass

class idleState(State):
    def on_event(self, event, boss):
        print("idle")
        if event == "player moves":
            return attackState()
        return self

class attackState(State):
    def on_event(self, event, boss):
        print("attack")
        if event == "low health" or event == "player attacks":
            return defendState()
        # shoot at player
        return self
            
class defendState(State):
    def on_event(self, event, boss):    
        print("defend")        
        if event == "player stops attack":
            return attackState()
        # move away from player
        return self

class Boss(object):
    def __init__ (self, maxWidth, maxHeight):
        # randomly generates boss in the room
        self.x = random.randint(0, maxWidth)
        self.y = random.randint(0, maxHeight) 
        self.mass = 50
        # initialises the starting state
        self.state = idleState() 

    def on_event(self, event):
        # assigns the event to the particular state it is in
        self.state = self.state.on_event(event, self)


def runGame():
    boss = Boss(10, 10)
    boss.on_event("player moves")
    boss.on_event("player attacks")

runGame()

###############################################################


# determines the final position of two objects after collision
def collision(a, b):
    totalMomentum = a.mass * a.speed - b.mass * b.speed 
    totalKE = 0.5*a.mass*a.speed**2 + 0.5*b.mass*b.speed**2
    # aFinalSpeed, bFinalSpeed 
    pass

def modifySpeed(playerSpeed, playerDirection, windSpeed):
    pass
