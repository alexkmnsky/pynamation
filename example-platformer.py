from pynamation import *
import time
from math import *
from random import *
st = time.time()
width = 800
height = 600
gravity = 0.4
count = 0
airState = True
paused = False
gameOver = False
groundHeight = height-100
createCanvas(width,height)
title("Platformer Example")
r = rect(0,0,width,height,fill="white")
distance = text(width - 100,50,text="0.0m", fontSize=24)
pauseText = text(width/2,100,text="")
tt = time.time()
obstacleTimer = 50

def returnLongVariable(obj):
    return Image(("assets/example-platformer/running", "gif"),obj.pos.x,obj.pos.y,amount=9,delay=2,zoom=-4,anchor="n")

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def add(self,other):
        self.x += other.x
        self.y += other.y

class Player:
    def __init__(self):
        self.jumpForce = 10
        self.dead = False
        self.w = 50
        self.h = 125
        self.pos = Vector(self.w + 100,groundHeight-self.h)
        self.vel = Vector(0,0)
        self.acc = Vector(0,0)
        self.shape = returnLongVariable(self)

    def resetShape(self):
        self.shape = returnLongVariable(self)

    def applyForce(self,forceX,forceY):
        force = Vector(forceX,forceY)
        self.acc.add(force)

    def jump(self,event):
        if(event.keysym == "space" and self.vel.y == 0):
            self.vel.y = -self.jumpForce

    def collide(self,obs):
        if(len(obs) > 0):
            for o in obs:
                if(self.pos.x + self.w > o.x and self.pos.x < o.x + o.w):
                    if(self.pos.y + self.w > o.y and self.pos.y < o.y + o.h):
                        canvasFunction().itemconfig(o.shape,fill="red")
                        self.dead = True
                        playSound("assets\example-platformer\chord.wav")
                        return True
            return False
    
    def update(self):
        global airState
        if not self.dead:
            self.shape.animate(self.vel.x,self.vel.y,isTrigger=airState)
        self.pos.add(self.vel)
        self.vel.add(self.acc)
        self.acc.x *= 0
        self.acc.y *= 0

        if(self.pos.y + self.h >= groundHeight):
            self.vel.y = 0

        if(self.vel.y == 0):
            airState = True
        else:
            airState = False

class Obstacle:
    def __init__(self):
        self.w = 50
        self.h = 100
        self.x = width
        self.y = groundHeight - self.h
        self.xVel = -7
        self.shape = rect(self.x,self.y,self.w,self.h,tag="gameObject")
    
    def update(self):
        self.x += self.xVel
        canvasFunction().move(self.shape,self.xVel,0)

player = Player()
obstacles = []

def pauseGame(event):
    global paused
    global tt
    global st
    if(paused):
        paused = False
        st = tt
        canvasFunction().itemconfig(pauseText,text="")
    else:
        paused = True
        tt = time.time()
        canvasFunction().itemconfig(pauseText,text="Game Paused")

def resetGame(event):
    global gameOver
    global obstacles
    global st
    global player
    gameOver = False
    canvasFunction().delete(player.shape.itself)
    canvasFunction().delete("gameObject")
    player = Player()
    tk.bind("<KeyPress-space>", player.jump)
    obstacles = []
    st = time.time()
    
obstacles.append(Obstacle())
ground = rect(0,groundHeight,width,height-groundHeight,fill="white")
        
def frameUpdate(): 
    global player
    global gameOver
    global count
    global obstacleTimer
    if(not paused and not gameOver):
        canvasFunction().itemconfig(distance,text=str(round((time.time() - st)*2,1)) + "m")
        if(count % obstacleTimer == 0):
            obstacles.append(Obstacle())
            count = 0
            obstacleTimer = floor(random() * 100) + 25
        player.applyForce(0,gravity)
        if player.collide(obstacles):
            gameOver = True
                    
        player.update()
        for o in obstacles[::-1]:
            o.update()
            if(o.x < -o.w):
                obstacles.remove(o)
        count += 1
    displayFrameRate(time.time(),50,50,color="black")
    canvasFunction().after(getFrameDelay(),frameUpdate)

frameUpdate()

tk.bind("<KeyPress-space>", player.jump)
tk.bind("<KeyPress-p>",pauseGame)
tk.bind("<KeyPress-r>",resetGame)

tk.mainloop()
