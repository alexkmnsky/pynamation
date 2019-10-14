from pynamation import *
from random import *
from math import *
import time
width = 800
height = 600
createCanvas(width,height)

title("Boids Example")
setFrameRate(63)

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.mag = sqrt(pow(self.x,2)+pow(self.y,2))
        self.angle = atan2(self.y,self.x)

    def setMag(self,value):
        self.mag = value
        self.x = cos(self.angle) * self.mag
        self.y = sin(self.angle) * self.mag

    def limit(self,value):
        if(self.mag > value):
            self.mag = value
            self.x = cos(self.angle) * self.mag
            self.y = sin(self.angle) * self.mag

    def add(self,other):
        self.x += other.x
        self.y += other.y
        self.mag = sqrt(pow(self.x,2)+pow(self.y,2))
        self.angle = atan2(self.y,self.x)
        
    def mult(self,other):
        if(type(other) == Vector):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        self.mag = sqrt(pow(self.x,2)+pow(self.y,2))
        self.angle = atan2(self.y,self.x)
            
    @staticmethod
    def sub(a,b):
        c = Vector(a.x,a.y)
        c.x -= b.x
        c.y -= b.y
        c.mag = sqrt(pow(c.x,2)+pow(c.y,2))
        c.angle = atan2(c.y,c.x)
        return c
        
        
class Particle:
    def __init__(self,x,y):
        self.r = 10
        self.pos = Vector(x,y)
        self.vel = Vector(0,0)
        self.acc = Vector(0,0)
        self.seekSpeed = 4
        self.seekForce = 0.05
        self.repelFactor = 2
        self.shape = ellipse(self.pos.x,self.pos.y,self.r*2,self.r*2,fill="grey")


    def applyForce(self,forceX,forceY):
        force = Vector(forceX,forceY)
        self.acc.add(force)

    def seek(self,targetX,targetY):
        target = Vector(targetX,targetY)
        desired = Vector.sub(target,self.pos)
        desired.setMag(1)
        desired.mult(self.seekSpeed)
        steer = Vector.sub(desired,self.vel)
        steer.limit(self.seekForce)
        self.applyForce(steer.x,steer.y)

    def repel(self,targetX,targetY):
        target = Vector(targetX,targetY)
        desired = Vector.sub(target,self.pos)
        desired.setMag(1)
        desired.mult(self.seekSpeed)
        steer = Vector.sub(desired,self.vel)
        steer.limit(self.seekForce)
        steer.mult(-1)
        steer.mult(self.repelFactor)
        self.applyForce(steer.x,steer.y)  

    def push(self,others):
        desiredSeperation = self.r*2
        s = Vector(0,0)
        count = 0
        for other in others:
            if(self.pos.x != other.pos.x):
                dist = sqrt(pow(self.pos.x-other.pos.x,2)+pow(self.pos.y-other.pos.y,2))
                if(dist < desiredSeperation):
                    diff = Vector.sub(self.pos,other.pos)
                    diff.setMag(1)
                    diff.mult(1/dist)
                    s.add(diff)
                    count += 1

        s.mult(5)
        self.applyForce(s.x*count,s.y*count)

    def update(self):

        mx = getMousePos("x")
        my = getMousePos("y")
        self.pos.add(self.vel)
        self.vel.add(self.acc)
        self.acc.mult(0)
        canvasFunction().move(self.shape,self.vel.x,self.vel.y)



particles = []
for i in range(1):
    particles.append(Particle(10 + (width-10*2)*random(),10+(height-10*2)*random()))

def update():
    displayFrameRate(time.time(),5,5,"black")
    if(getButtonInput() == 1):
        particles.append(Particle(getMousePos("x"),getMousePos("y")))
                         
    for p in particles:
        p.push(particles)
        p.update()
        p.seek(getMousePos("x"),getMousePos("y"))

    canvasFunction().after(getFrameDelay(),update)

update()
tk.bind("<Motion>", mousePos)
tk.bind("<ButtonPress>", buttonPress)
tk.bind("<ButtonRelease>", buttonRelease)
tk.mainloop()
