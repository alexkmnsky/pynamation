
from tkinter import *
from math import *
import winsound

tk = Tk()

canvas = None
mouseX = 0
mouseY = 0
currentKey = None
currentButton = None
frameRate = 63
frameDelay = 1000//frameRate
startTime = 1
globalTag = 0

# Image rendering with multi-texture animation support
# Avoid using img()
class Image:

    def __init__(self, image, x, y, amount = 1, zoom = 1, anchor = "nw", delay = 1, tags=("",)):

        # Store all images for future reference (more than 1 if animated)
        self.images = []
        for i in range(amount):
            self.images.append(PhotoImage(file = image[0]+str(i) + "." + image[1]))

        self.counter = 0
        self.delayCounter = 0
        self.delay = delay
        self.amount = amount

        # Zoom the image if the value specified is greater than 1
        if(zoom != 1 and zoom > 0):
            for i in range(len(self.images)):
                self.images[i] = self.images[i].zoom(zoom)

        # Zoom out the image if the value specified is less than 1
        elif(zoom < 0):
            for i in range(len(self.images)):
                self.images[i] = self.images[i].subsample(zoom*-1)
        
        # Draw the image
        self.itself = canvas.create_image(x, y, image = self.images[0], anchor=anchor, tags = (str(globalTag),) + tags)

    def animate(self, xVel, yVel, isTrigger = True):

        # Reset the counter once the final image is reached
        if(self.counter > self.amount-1):
            self.counter = 0

        # Only cycle through images unless specified otherwise
        if(isTrigger == True):
            canvas.itemconfig(self.itself, image = self.images[self.counter])
            self.delayCounter += 1
            if(self.delayCounter == self.delay):
                self.counter += 1
                self.delayCounter = 0

        # Update the position of the image
        canvas.move(self.itself, xVel, yVel)

# Simplified shape rendering
# Avoid using rect(), ellipse(), etc.
class Shape:

    @staticmethod
    def rectangle(x, y, width, height, fill="white", border=("black", 1), anchor="nw", tags=("",)):
        global globalTag
        bx = x + width
        by = y + height
        shape = canvas.create_rectangle(x, y, bx, by, fill=fill, outline=border[0], width=border[1], tags = (str(globalTag),) + tags)
        globalTag += 1
        return shape

    @staticmethod
    def ellipse(x, y, width, height, fill="white", border=("black", 1), anchor="nw", tags=("",)):
        global globalTag
        bx = x + width/2
        by = y + height/2
        tx = x - width/2
        ty = y - height/2
        shape = canvas.create_oval(tx, ty, bx, by, fill=fill, outline=border[0], width=border[1], tags = (str(globalTag),) + tags)
        globalTag += 1
        return shape

    @staticmethod
    def polygon(verticies,fill="white", border=("black", 1), tags=("",)):
        global canvas
        shape = canvas.create_polygon(verticies, fill = fill, outline = border[0], width = border[1], tags = (str(globalTag),) + tags)
        return shape

def title(windowTitle):
    tk.title(windowTitle)

def setFrameRate(val):
    global frameRate
    global frameDelay
    frameRate = val
    frameDelay = 1000//frameRate

def displayFrameRate(t,x,y,color="yellow",anchor="nw"):
    global startTime
    canvas.delete("frameRate")
    text(x, y, tag="frameRate", fill=color, text = str(str(round((1/ (t - startTime)))) + " FPS"), anchor=anchor)
    startTime = t

# Requires:
# import time

def deleteShape(s):
    canvas.delete(s)

def changeFill(s,fill):
    canvas.itemconfig(s,fill=fill)

def getFrameDelay():
    return frameDelay

def createCanvas(w,h):
    global canvas
    canvas = Canvas(tk,width=w,height=h)
    canvas.pack()

def changeText(t,nt):
    canvas.itemconfig(t,text=nt)

def canvasFunction():
    global canvas
    return canvas

def rect(x,y,w,h,fill="white",tag=""): # Deprecated, use Shape.rectangle()
    global canvas
    global globalTag
    bx = x + w
    by = y + h
    r = canvas.create_rectangle(x,y,bx,by,fill=fill,tags=(str(globalTag),tag))
    globalTag += 1
    return r

def ellipse(x,y,w,h,fill="white",tag=""): # Deprecated, use Shape.ellipse()
    global globalTag
    oval = canvas.create_oval(x - (w/2),y-(h/2),x + (w/2), y + (w/2),fill=fill,tags=(str(globalTag),tag))
    globalTag += 1
    return oval

def polygon(verticies,fill="white",outline="green"): # Deprecated, use Shape.polygon()
    global canvas
    poly = canvas.create_polygon(verticies,fill=fill,outline=outline)
    return poly
    
def text(x,y,text="Hello World",fill="black",fontFace="Arial", fontSize=12, fontStyle="", anchor="center",tag=""):
    text = canvas.create_text(x,y,text=text,fill=fill,font=(fontFace, fontSize, fontStyle),anchor=anchor,tag=tag)
    return text

def img(image,x,y): # Deprecated, use Image()
    i = canvas.create_image(x, y, image=image, anchor=NW)
    return i

def playSound(soundFile):
    winsound.PlaySound(soundFile,winsound.SND_ASYNC)

def setCursor(cursor):
    tk.config(cursor=cursor)

def mousePos(event):
    global mouseX
    global mouseY
    mouseX = event.x
    mouseY = event.y

def getMousePos(option):
    if(option == "x"):
        return mouseX
    elif(option == "y"):
        return mouseY
    return [mouseX,mouseY]

# Requires: tk.bind("<Motion>", mousePos)

def keyPress(event):
    global currentKey
    currentKey = event.keysym

def keyRelease(event):
    global currentKey
    currentKey = None
    
def getKeyInput():
    return currentKey

# Requires lines:
# tk.bind("<KeyPress>", keyPress)
# tk.bind("<KeyRelease>", keyRelease)

def buttonPress(event):
    global currentButton
    currentButton = event.num

def buttonRelease(event):
    global currentButton
    currentButton = None

def getButtonInput():
    return currentButton

# Requires lines:
# tk.bind("<ButtonPress>", buttonPress)
# tk.bind("<ButtonRelease>", buttonRelease)
