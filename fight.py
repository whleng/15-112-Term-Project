import random

# referenced structure from 
# https://dev.to/karn/building-a-simple-state-machine-in-python

class State(object):
    def __init__(self):
        print("Current state: ", str(self))

    def __rep__(self):
        return self.__class__.__name__
        
    def on_event(self, event):
        # do some tasks according to the diff events that could occur at this state
        # set the boss to another state
        pass

class idleState(State):
    def on_event(self, event):
        pass

class attackState(State):
    def on_event(self, event):
        pass

class defendState(State):
    def on_event(self, event):            
        pass

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
        self.state = self.state.on_event(event)

# determines the final position of two objects after collision
def collision(a, b):
    totalMomentum = a.mass * a.speed - b.mass * b.speed 
    totalKE = 0.5*a.mass*a.speed**2 + 0.5*b.mass*b.speed**2
    # aFinalSpeed, bFinalSpeed 
    pass

def modifySpeed(playerSpeed, playerDirection, windSpeed):
    pass