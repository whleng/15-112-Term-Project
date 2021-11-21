
from cmu_112_graphics import *

# cited from 
# http://www.cs.cmu.edu/~112/notes/notes-graphics.html#installingModules
def appStarted(app):
    # # path = "Graphics/player.png"
    # spriteRight = app.loadImage(r"Graphics/walkingRight.png")
    # spriteLeft = app.loadImage(r"Graphics/walkingLeft.png")
    # app.sprites = {'left': [], 'right': [], 'up': [], 'down': []}
    # for i in range(9):
    #     # sprite = spritestrip.crop((i*198, 0, (i+1)*60+5, 63))
    #     # sprite = spritestrip.crop((i*(60)+5, 0, (i+1)*60+5, 63))
    #     # sprite = spritestrip.crop((i*(30+5), 0, i*(30+5)+30, 63))
    #     sprite = spriteRight.crop((i*(45+18), 0, i*(45+18)+45, 63))
    #     app.sprites['right'].append(sprite)
    #     sprite = spriteLeft.crop((i*(45+18), 0, i*(45+18)+45, 62))
    #     app.sprites['left'].append(sprite)
    # app.spriteCounter = 0
    # app.dir = "right"

    # referenced from Tze Hng Loke (tloke)

    app.explosionSpriteSheet = app.loadImage('Graphics/player.png')
    imageWidth, imageHeight = app.explosionSpriteSheet.size
    app.cellHeight = 500
    app.explosionHeightfactor = app.cellHeight / imageHeight
    app.explosionsprite = []
    rows = 21
    cols = 13
    for row in range(rows):
        for col in range(cols):
            sprite = app.explosionSpriteSheet.crop((imageWidth/cols*col, imageHeight/rows*row, imageWidth/cols*(col+1) , imageHeight/rows*(row+1)))
            scaledsprite = app.scaleImage(sprite, app.explosionHeightfactor*1.9)
            app.explosionsprite.append(scaledsprite)
    app.spriteCounter = 0

def timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.explosionsprite)

def keyPressed(app, event):
    if event.key == "Left":
        app.dir = "left"
    elif event.key == "Right":
        app.dir = "right"

def redrawAll(app, canvas):
    sprite = app.explosionsprite[app.spriteCounter]
    canvas.create_image(200, 200, image=ImageTk.PhotoImage(sprite))
    # sprite = app.sprites[app.dir][app.spriteCounter]
    # canvas.create_image(200, 200, image=ImageTk.PhotoImage(sprite))
    # print(app.spriteCounter)

runApp(width=400, height=400)
