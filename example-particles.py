from pynamation import *
from random import *
from math import *
from time import time

# Global Variables:

width = 800
height = 600
particleNum = 20
gameTimer = None
gameOver = False
setFrameRate(63)
createCanvas(width,height)
title("Particle Clicker")
colors = ["red","green","blue","purple","yellow","brown","orange","pink","turquoise","grey","indigo","violet"]
gameColor = choice(colors)
introScreen = True
defaultCursor = "arrow"
gameCursor = "tcross"
st = 0

# Images:

images = []
images.append(PhotoImage(file="assets/example-particles/grid.gif"))
images[0] = images[0].zoom(2)

class Particle:
    def __init__(self):
        self.r = 25
        self.x = self.r + random()*(width-self.r*2-2) + 1
        self.y = self.r + random()*(height-self.r*2-2) + 1
        self.xVel = 10 * random() - 5
        self.yVel = 10 * random() - 5
        self.shape = ellipse(self.x,self.y,self.r*2,self.r*2,fill=gameColor)

    def update(self):
        self.x += self.xVel
        self.y += self.yVel
        if(self.x + self.r >= width or self.x - self.r < 0):
            self.xVel *=  -1
        if(self.y + self.r >= height or self.y - self.r < 0):
            self.yVel *= -1
        canvasFunction().move(self.shape,self.xVel,self.yVel)

def delParticles(event):
    global particles
    mx = getMousePos("x")
    my = getMousePos("y")
    for p in particles[::-1]:
        dist = sqrt(pow(mx-p.x,2)+pow(my-p.y,2))
        if(dist < p.r):
            if(event.num == 1):
                deleteShape(p.shape)
                particles.remove(p)
                break

particles = []

setCursor(defaultCursor)
backgroundImg = img(images[0],0,0)
timer = text(width/2,50,fill="black",text=None,fontSize=24,fontFace="Arial Black",tag="timer")

titleText = text(width/2,height/4,text="Particle Clicker",fontSize=48,fontFace="Arial Black",tag="splash")
subtitleText = text(width/2,height/4+50,text="Click the particles as fast as you can!",fontSize=18,fontFace="Arial",tag="splash")

startButtonWidth = 150
startButtonHeight = 60
startButtonFill = "white"
startButtonHoverFill = "#dddddd"
startButton = rect(width/2-startButtonWidth/2,height/2-startButtonHeight/2,startButtonWidth,startButtonHeight,fill=startButtonFill,tag="splash")
startButtonText = text(width/2,height/2,text="Play",fontSize=24,fontFace="Arial",tag="splash")

def summonParticles():
    for i in range(particleNum):
        particles.append(Particle())

def setup():
    playSound("assets\example-particles\gameMusic1.wav")
    pass

def move():
    global introScreen
    global gameTimer
    global st
    if(st % 1120 == 0):
        playSound("assets\example-particles\gameMusic1.wav")
    displayFrameRate(time(),5,5,color="black",anchor="nw")
    if(not introScreen):
        for p in particles:
            p.update()
        if((len(particles)) > 0):
            changeText(timer, round((time() - gameTimer),1))
        else:
            global gameOver
            if gameOver == False:
                changeText(timer, str("Game over! Your time: " + str(round((time() - gameTimer),3))))
            gameOver = True
    else:
        mx = getMousePos("x")
        my = getMousePos("y")
        startLeft = width/2-startButtonWidth/2
        startRight = width/2+startButtonWidth/2
        startTop = height/2-startButtonHeight/2
        startBottom = height/2+startButtonHeight/2
        if(mx > startLeft) and (mx < startRight) and (my > startTop) and (my < startBottom):
            changeFill(startButton,startButtonHoverFill)
            setCursor("hand2")
            if(getButtonInput() == 1):
                canvasFunction().delete("splash")
                summonParticles()
                setCursor(gameCursor)
                introScreen = False
                gameTimer = time()
                tk.bind("<Button-1>", delParticles)
                tk.bind("<KeyPress-r>", resetGame)
        else:
            setCursor(defaultCursor)
            changeFill(startButton,startButtonFill)
    canvasFunction().tag_raise(timer)
    st += 1
    canvasFunction().after(getFrameDelay(),move)

def resetGame(event):
    global particles
    global gameTimer
    global gameOver
    global gameColor
    if(not introScreen):
        if(event.char == "r"):
            for p in particles[::-1]:
                deleteShape(p.shape)
            particles = []
            summonParticles()
            gameTimer = time()
            gameOver = False
            gameColor = choice(colors)

setup()
move()

tk.bind("<Motion>", mousePos)
tk.bind("<ButtonPress>", buttonPress)
tk.bind("<ButtonRelease>", buttonRelease)

tk.mainloop()
