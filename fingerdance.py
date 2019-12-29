#import Leap, sys, thread, time 
import os, sys, inspect, thread, time
sys.path.insert(0, "C:\Users\apple\Desktop\LeapSDK\lib")
import Leap
import random
import pyaudio
import wave
import sys
import pygame

from array import array
from struct import pack
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from Tkinter import *

#########################################
#LeapMotionApp.py Citation Comment:
#Lines 000-370: Original code
#Lines 370-390: From 15-112 mini-class file LeapMotionDemo
#Lines 390-570: Original code
#Lines 570-595: From https://www.python-course.eu/tkinter_entry_widgets.php
#Lines 595-650: Original code
#Lines 650-690: From 15-112 class website https://www.cs.cmu.edu/~112/index.html
#########################################

def init(data):
    #the first 4 lines are cited from class code file LeapMotionDemo
    data.controller = Leap.Controller()
    data.frame = data.controller.frame()
    data.fingerNames = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    data.boneNames = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    
    data.margin = 5
    data.CADwidth = [1.5,3,8]
    data.timer = 0
    data.leftFingers = []
    data.rightFingers = []
    data.buttonColor = "salmon"
    data.bgc = "grey"
    data.fingerColor = ["red","yellow","blue","white","white","red","yellow","blue","white","white"]
    data.ringColorA = "white"
    data.ringColorB = "white"
    
    data.records = {}

    #the order of each 2 buttons is top, right, bottom, left.
    data.buttonbackPoints =[
                        (165,0,165,40,120,100,280,100,235,40,235,0,165,0),
                        (965,0,965,40,920,100,1080,100,1035,40,1035,0,965,0),
                        (530,265,480,265,430,220,430,380,480,335,530,335,530,265),
                        (670,335,720,335,770,380,770,220,720,265,670,265,670,335),
                        (165,595,165,555,120,495,
                        280,495,235,555,235,595,165,595),
                        (965,595,965,555,920,495,
                        1080,495,1035,555,1035,595,965,595),
                        ]
    data.buttonPoints = [(165,0,165,40,120,100,
                        100,100,100,0,300,0,300,100,
                        280,100,235,40,235,0,165,0),
                        (965,0,965,40,920,100,
                        900,100,900,0,1100,0,1100,100,
                        1080,100,1035,40,1035,0,965,0),
                        
                        (530,265,480,265,430,220,
                        430,200,530,200,530,400,430,400,
                        430,380,480,335,530,335,530,265),
                        (670,335,720,335,770,380,
                        770,400,670,400,670,200,770,200,
                        770,220,720,265,670,265,670,335),
                        
                        (165,595,165,555,120,495,
                        100,495,100,595,300,595,300,495,
                        280,495,235,555,235,595,165,595),
                        (965,595,965,555,920,495,
                        900,495,900,595,1100,595,1100,495,
                        1080,495,1035,555,1035,595,965,595),
                        ]
    data.ringIndex = 0
    data.ringAX1 = 0
    data.ringAY1 = 0
    data.ringAX2 = 0
    data.ringAY2 = 0
    data.ringBX1 = 0
    data.ringBY1 = 0
    data.ringBX2 = 0
    data.ringBY2 = 0
    data.ringSpeed = 2
    
    data.playbegin = False
    data.band = False

def initScore(data):
    #player1(left)
    data.scoreA = 0
    #continuely touch score
    data.xscoreA = 0
    data.XscoreA = 0
    data.bloodA = 340
    data.energyA = 0
    data.lifenumA = 1
    data.touchA = False
    data.wrongtouchA = False
    data.longtouchA = False
    data.gameoverA = False
    data.gameboomA = False
    data.playbeginA = False
        
    #player2(right)
    data.scoreB = 0
    data.xscoreB = 0
    data.XscoreB = 0
    data.bloodB = 340
    data.energyB = 0
    data.lifenumB = 1
    data.touchB = False
    data.wrongtouchB = False
    data.longtouchB = False
    data.gameoverB = False
    data.gameboomB = False
    data.playbeginB = False
    
    #common
    data.instruct = False
    data.showrank = False
    data.ready = True
    data.go = True
    
def mousePressed(event, data):
    #at the beginning, press the play button, game begins
    if((event.x>data.width/2-100) and (event.x<data.width/2+100) and 
        (event.y>data.height/3*2-30) and (event.y<data.height/3*2+30)):
            data.playbegin = True
            #set all score default value back
            initScore(data)
            playMusic(data)
    #press the guide button, show instructions of the game
    if((event.x>data.width/4-100) and (event.x<data.width/4+100) and 
        (event.y>data.height/3*2-30) and (event.y<data.height/3*2+30)):
            data.instruct = not data.instruct
    #press the rank button, show rank file
    if((event.x>data.width/4*3-100) and (event.x<data.width/4*3+100) and 
        (event.y>data.height/3*2-30) and (event.y<data.height/3*2+30)):
            data.showrank = not data.showrank
            

def playMusic(data):
    pygame.mixer.init()
    pygame.mixer.music.load("dontstop2.wav")
    pygame.mixer.music.play()

def stopMusic(data):
    if data.gameoverA and data.gameoverB:
        pygame.mixer.init()
        pygame.mixer.music.load("dontstop2.wav")
        pygame.mixer.music.stop()
    if not data.playbegin:
        pygame.mixer.init()
        pygame.mixer.music.load("dontstop2.wav")
        pygame.mixer.music.stop()
        
        
def keyPressed(event, data):
    if (event.char == "p"):
        data.playbegin = False
    pass
    
def ringPosition(data):
    #randomly choose a button on the left part to run rings
    data.ringIndex = random.choice([0,2,4])
    data.ringColorA = random.choice(["red", "yellow", "blue"])
    data.ringColorB = data.ringColorA
    
    #for different button postion, different begin position of the ring
    lp = data.buttonPoints[data.ringIndex]
    data.ringAX1 = lp[8]
    data.ringAY1 = lp[9]
    data.ringAX2 = lp[10]
    data.ringAY2 = lp[11]
    #corresponding ring generation on the right part
    rp = data.buttonPoints[data.ringIndex+1]
    data.ringBX1 = rp[8]
    data.ringBY1 = rp[9]
    data.ringBX2 = rp[10]
    data.ringBY2 = rp[11]
    
def timerFired(data):
    updateLeapMotionData(data)
    printLeapMotionData(data)
    stopMusic(data)
    data.timer += 1
    ringMove(data)
    ringleftTouch(data)
    ringrightTouch(data)
    if data.playbegin:
        #after the first second, generate a ring or band
        if data.timer % 40 == 0:
            data.ready = False
        #every 5 second, generate a ring for short touch
        if data.timer % 50 == 0:
            data.go = False
            if not data.go:
                ringPosition(data)
                scores(data)
                #after touch, the ring would disappear forever
                data.touchA = False
                data.touchB = False
        #every 20 second, generate a band for long rouch
        if data.timer % 200 == 0:
            data.band = True

#caculate total score, xScore, lifeNum, energy
def scores(data):
    #when continuously right touch, x score increases,else back to 0
    #every 5 success, energy pipe will be full and life increases one.
    x = 10
    
    #playerA
    if data.touchA:
        data.scoreA += 1
        data.xscoreA += 1
        data.energyA += 1
        if data.xscoreA > data.XscoreA:
            data.XscoreA = data.xscoreA
        # when draw flow length, need to times 40 to amplify
    elif not data.go:
        data.xscoreA = 0
        if data.bloodA > 0:
            #if wrong touch, blood will decrease 2 times
            if data.wrongtouchA:
                data.bloodA -= 340/x*2
                data.wrongtouchA = False
            else:
                data.bloodA -= 340/x
        elif data.lifenumA > 0:
            data.lifenumA -= 1
            data.bloodA = 340
        elif data.lifenumA == 0:
            data.playbeginA = False
            data.gameoverA =True
    if data.energyA >= x:
        data.bloodA += 340/x*2
        data.energyA %= x
        
    #playerB
    if data.touchB:
        data.scoreB += 1
        data.xscoreB += 1
        data.energyB += 1
        if data.xscoreB > data.XscoreB:
            data.XscoreB = data.xscoreB
        # when draw, need to times 40 to amplify
    else:
        data.xscoreB = 0
        if data.bloodB > 0:
            #if wrong touch, blood will decrease 2 times
            if data.wrongtouchB:
                data.bloodB -= 340/x*2
            else:
                data.bloodB -= 340/x
        elif data.lifenumB > 0:
            data.lifenumB -= 1
            data.bloodB = 340
        elif data.lifenumB == 0:
            data.playbeginB = False
            data.gameoverB =True
    if data.energyB >= x:
        data.bloodB += 340/x*2
        data.energyB %= x
        

def ringMove(data):
    #for different button postion, different move pattern of the ring 
    i = data.ringIndex
    d = data.ringSpeed
    #left top button and right top button
    if i == 0:
        data.ringAY1 += d
        data.ringAY2 += d
        data.ringBY1 += d
        data.ringBY2 += d
    #middle button
    if i ==2:      
        data.ringAX1 -= d
        data.ringAX2 -= d
        data.ringBX1 += d
        data.ringBX2 += d  
    #bottom button
    if i == 4:       
        data.ringAY1 -= d
        data.ringAY2 -= d
        data.ringBY1 -= d
        data.ringBY2 -= d

#right color represent right finger
def ringleftTouch(data):
    i = data.ringIndex
    j = 0
    #check each finger point whether it is in area defined by the ring
    for point in data.leftFingers:
        #should be same scale as in def drawFinger
        x = (300+point[0])*2
        y = (450-point[1])*2
        #first check the finger touch the ring
        #different side has different check standard
        if i == 0:
            if ((x > data.ringAX1) and (x < data.ringAX2) 
            and (y < data.ringAY1)):
                #check the color of the finger and the ring
                if data.ringColorA == data.fingerColor[j]:
                    data.touchA = True
                else:
                    data.wrongtouchA = True
        elif i == 2:
            if ((y > data.ringAY1) and (y < data.ringAY2) 
            and (x > data.ringAX1)):
                #check the color of the finger and the ring
                if data.ringColorA == data.fingerColor[j]:
                    data.touchA = True
                else:
                    data.wrongtouchA = True       
        elif i == 4:
            if ((x > data.ringAX1) and (x < data.ringAX2)
            and (y > data.ringAY1)):
                #check the color of the finger and the ring
                if data.ringColorA == data.fingerColor[j]:
                    data.touchA = True
                else:
                    data.wrongtouchA = True
        j += 1
    
def ringrightTouch(data):
    i = data.ringIndex
    j = 0
    for point in data.rightFingers:                
        x = (300+point[0])*2
        y = (450-point[1])*2
        #first check the finger touch the ring
        #different side has different check standard 
        if i == 0:
            if ((x > data.ringBX1) and (x < data.ringBX2) 
            and (y < data.ringBY1)):
                #check the color of the finger and the ring
                if data.ringColorB == data.fingerColor[j]:
                    data.touchB = True
                else:
                    data.wrongtouchB = True
                    
        elif i == 2:
            if ((y < data.ringBY1) and (y > data.ringBY2) 
            and (x < data.ringBX1)):
                if data.ringColorB == data.fingerColor[j]:
                    data.touchB = True
                else:
                    data.wrongtouchB = True
                    
        elif i == 4:
            if ((x > data.ringBX1) and (x < data.ringBX2)
            and (y > data.ringBY1)):
                if data.ringColorB == data.fingerColor[j]:
                    data.touchB = True
                else:
                    data.wrongtouchB = True
        j += 1
        





#two functions below are cited from class code file LeapMotionDemo
def updateLeapMotionData(data):
    data.frame = data.controller.frame()
    
def printLeapMotionData(data):
    frame = data.frame
    data.leftFingers = []
    data.rightFingers = []
    # Get hands
    for hand in frame.hands:
        if hand.is_left:
            # Get fingers of left hand
            for finger in hand.fingers:
                #Get positin of finger
                bone = finger.bone(3)
                data.leftFingers += [(bone.next_joint[0],bone.next_joint[1])]
        else:
            # Get fingers of left hand
            for finger in hand.fingers:
                #Get positin of finger
                bone = finger.bone(3)
                data.rightFingers += [(bone.next_joint[0],bone.next_joint[1])]
  
def drawFinger(canvas, data):
    #scale the point to fit the canvas
    #draw left hand
    j = 0
    for point in data.leftFingers:
        x = (300+point[0])*2
        y = (450-point[1])*2
        if j == 0:
            canvas.create_oval(x-10,y-10,x+10,y+10, fill=data.fingerColor[j])
        elif j == 1:
            canvas.create_oval(x-10,y-10,x+10,y+10, fill=data.fingerColor[j])
        elif j == 2:
            canvas.create_oval(x-10,y-10,x+10,y+10, fill=data.fingerColor[j])
        j += 1
    
    #draw right hand
    j = 0
    for point in data.rightFingers:
        x = (300+point[0])*2
        y = (450-point[1])*2
        if j == 0:
            canvas.create_oval(x-10,y-10,x+10,y+10, fill=data.fingerColor[j])
        elif j == 1:
            canvas.create_oval(x-10,y-10,x+10,y+10, fill=data.fingerColor[j])
        elif j == 2:
            canvas.create_oval(x-10,y-10,x+10,y+10, fill=data.fingerColor[j])
        j += 1

def drawButton(canvas, data):
    for i in data.buttonPoints:
        canvas.create_polygon(i, fill="black")
def drawButtonback(canvas,data):
    for i in data.buttonbackPoints:
        canvas.create_polygon(i, fill=data.bgc)

def drawRing(canvas, data):
    if not data.gameoverA:
        canvas.create_line(data.ringAX1, data.ringAY1, 
        data.ringAX2, data.ringAY2, fill=data.ringColorA, width=data.CADwidth[2])
        if data.touchA:
            data.ringColorA="dim grey"
    if not data.gameoverB:
        canvas.create_line(data.ringBX1, data.ringBY1, 
        data.ringBX2, data.ringBY2, fill=data.ringColorB, width=data.CADwidth[2])
        if data.touchB:
            data.ringColorB="dim grey"

#DRAW the begining page of the game
def drawBegin(canvas,data):
    x2 = data.width/2
    x3 = data.width/3
    x4 = data.width/4
    y2 = data.height/2
    y3 = data.height/3
    y4 = data.height/4
    textcolor = "salmon4"
    framC = "dim gray"
    #draw buttons on the screen and text on it
    canvas.create_rectangle(data.margin,data.margin, data.width-data.margin, data.height-data.margin, width=data.CADwidth[-1], fill="white")
    canvas.create_rectangle(x4-100, y3*2-30, x4+100, y3*2+30, fill="salmon2")
    canvas.create_rectangle(x2-100, y3*2-30, x2+100, y3*2+30, fill="salmon2")
    canvas.create_rectangle(x4*3-100, y3*2-30, x4*3+100, y3*2+30, fill="salmon2")
    canvas.create_text(x2,y4,text="--------- Keep on Dancing ---------",fill=textcolor,font="Arial 80 bold")
    canvas.create_text(x2,y2-20,
    text="Student: Ruiji Sun\nClass: 15112\nDate: 12/06/2018",
    fill=textcolor,font="Arial 25")
    canvas.create_text(x4,y3*2,text="Guide",fill=textcolor,font="Arial 25  italic bold")
    canvas.create_text(x2,y3*2,text="Play",fill=textcolor,font="Arial 25 italic bold")
    canvas.create_text(x4*3,y3*2,text="Rank",fill=textcolor,font="Arial 25  italic bold")
    
    #when press instruct, draw below
    drawInstruct(canvas, data)
    showrank(canvas, data)

def drawInstruct(canvas, data):
    if data.instruct:
        canvas.create_rectangle(30,50,data.width-30,data.height/2+30, fill="salmon")
        canvas.create_text(data.width/2,data.height/4+15,
            text="1.Put you hand above your leap Motion.\n2.Moving band appears at where color change. \n3.Move your hand to touch the band at the end of button. \n4.Red pipe is life, once empty, life amount decreases. \n5.Blue pipe is touch, once full, life amount increases.",
            fill="salmon4",font="Arial 40 italic bold")
    
def drawGameover(canvas, data):
    #when gameover, draw below
    if data.gameoverA:
        canvas.create_text(200,data.height/2-40,
            text="PLAYER-A",fill="salmon4",font="Arial 20 bold")
        canvas.create_text(200,data.height/2,
            text="Game Over",fill="salmon4",font="Arial 50 bold")
        canvas.create_text(200,data.height/2+40,
            text="Final Score: %s"%data.scoreA,
            fill="red",font="Arial 20 bold")
        canvas.create_text(200,data.height/2+65,
            text="Highest Flow:%s"%data.XscoreA,
            fill="blue",font="Arial 20 bold")
            
    if data.gameoverB:
        canvas.create_text(1000,data.height/2-40,
            text="PLAYER-B",fill="salmon4",font="Arial 20 bold")
        canvas.create_text(1000,data.height/2,
            text="Game Over",fill="salmon4",font="Arial 50 bold")
        canvas.create_text(1000,data.height/2+40,
            text="Final Score:%s"%data.scoreB,
            fill="red",font="Arial 20 bold")
        canvas.create_text(1000,data.height/2+65,
            text="Highest Flow: %s"%data.XscoreB,
            fill="blue",font="Arial 20 bold")

#based on function in timefired
def drawReadygo(canvas,data):
    if data.playbegin:
        if data.ready:
            canvas.create_text(200,data.height/2-40,
                text="PLAYER-A",fill="salmon4",font="Arial 20 bold")
            canvas.create_text(1000,data.height/2-40,
                text="PLAYER-B",fill="salmon4",font="Arial 20 bold")
            canvas.create_text(200,data.height/2,text="Ready?",fill="salmon4",font="Arial 50 bold")
            canvas.create_text(1000,data.height/2,text="Ready?",fill="salmon4",font="Arial 50 bold")
        elif data.go:
            canvas.create_text(200,data.height/2-40,
                text="PLAYER-A",fill="salmon4",font="Arial 20 bold")
            canvas.create_text(1000,data.height/2-40,
                text="PLAYER-B",fill="salmon4",font="Arial 20 bold")
            canvas.create_text(200,data.height/2,text="Go!",fill="salmon4",font="Arial 50 bold")
            canvas.create_text(1000,data.height/2,text="Go!",fill="salmon4",font="Arial 50 bold")
         

#draw scores, success times, reb(blood) pipe, blue(energy) pipe.
def drawInterface(canvas, data):
    drawDashboard(canvas, data)
    canvas.create_text(data.width/2,data.height/2,
        text="press 'p'\nto restart", fill="black",font="Arial 20 italic")

def drawDashboard(canvas, data):
    canvas.create_rectangle(data.margin,data.margin, data.width-data.margin, data.height-data.margin, width=data.CADwidth[-1])
    #draw top frame
    canvas.create_rectangle(430,5, 770,150, width=data.CADwidth[1])
    canvas.create_line(430,35, 770,35, width=data.CADwidth[0])
    canvas.create_line(430,60, 770,60, width=data.CADwidth[0])
    canvas.create_line(430,120, 770,120, width=data.CADwidth[0])
    canvas.create_line(600,60, 600,150, width=data.CADwidth[0])
    #draw scores
    canvas.create_text(515,135,
        text="Score", fill="black",font="Arial 20")
    canvas.create_text(515,90,
        text=data.scoreA, fill="salmon2",font="Arial 50 bold")
    canvas.create_text(685,135,
        text="Flow", fill="black",font="Arial 20")
    canvas.create_text(685,90,
        text="x%s"%data.xscoreA, fill="blue",font="Arial 50 bold")
    #draw "pipe", which is score visualization
    canvas.create_rectangle(430,35, 430+data.bloodA,60, fill="red")
    canvas.create_rectangle(430,5, 430+data.energyA*34,35, fill="blue")
    canvas.create_text(600,45,
        text="life:x%s"%data.lifenumA, fill="black",font="Arial 20")
    canvas.create_text(600,20,
        text="PLAYER-A", fill="black",font="Arial 20 bold")
        
    #draw bottom frame
    canvas.create_rectangle(430,450, 770,595, width=data.CADwidth[1])
    canvas.create_line(430,480, 770,480, width=data.CADwidth[0])
    canvas.create_line(430,505, 770,505, width=data.CADwidth[0])
    canvas.create_line(430,565, 770,565, width=data.CADwidth[0])
    canvas.create_line(600,505, 600,595, width=data.CADwidth[0])

    canvas.create_rectangle(430,450, 430+data.energyB*34,480, fill="blue")    
    canvas.create_rectangle(430,480, 430+data.bloodB,505, fill="red")

    canvas.create_text(600,465,
        text="PLAYER-B", fill="black",font="Arial 20 bold")
    canvas.create_text(600,490,
        text="life:x%s"%data.lifenumB, fill="black",font="Arial 20")
    canvas.create_text(515,575,
        text="Score", fill="black",font="Arial 20")
    canvas.create_text(685,575,
        text="Flow", fill="black",font="Arial 20")
    canvas.create_text(515,530,
        text=data.scoreB, fill="salmon2",font="Arial 50 bold")
    canvas.create_text(685,530,
        text="x%s"%data.xscoreB, fill="blue",font="Arial 50 bold")
  
#Below function is from https://www.python-course.eu/tkinter_entry_widgets.php
def drawRank(canvas, data):
    if data.gameoverA and data.gameoverB:
        def record():
            data.records[data.scoreA] = e1.get()
            data.records[data.scoreB] = e2.get()
            print(data.records)
            rank(data)
            e1.delete(0,END)
            e2.delete(0,END)
        
        master = Tk()
        Label(master, text="PLAYER-A").grid(row=0)
        Label(master, text="PLAYER-B").grid(row=1)
        
        e1 = Entry(master)
        e2 = Entry(master)
        
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        
        Button(master, text='Quit', command=master.destroy).grid(row=3, column=0, sticky=W, pady=4)
        Button(master, text='OK', command=record).grid(row=3, column=1, sticky=W, pady=4)
            
        mainloop( )
        
#write a local txt file with scores information 
def rank(data):
    l = []
    with open("Record.txt", "w") as wf:
        for key in data.records:
            print(key)
            l += [key]
        l.sort()
        l.reverse()
        i = 1
        for item in l:
            wf.write("Rank-%s, Name-%s:, Score-%s\n" % (i,data.records[item],item))    
            i += 1     
               
#show on the begining page, if click
def showrank(canvas, data):
    i = 0
    if data.showrank:
        canvas.create_rectangle(30,50,data.width-30,data.height/2+30, fill="salmon")
        with open("Record.txt", "r") as rf:
            for line in rf:
                canvas.create_text(data.width/2,data.height/4+i,
                    text=line, fill="salmon4",font="Arial 40 italic bold")
                i += 50
    


def redrawAll(canvas, data):
    drawInterface(canvas,data)
    drawReadygo(canvas,data)

    drawButtonback(canvas,data)
    drawRing(canvas, data)
    drawButton(canvas, data)
    
    drawFinger(canvas, data)
    
    drawGameover(canvas, data)
    drawRank(canvas, data)
    if not data.playbegin:
        drawBegin(canvas,data)
       
    

####################################
# use the run function as-is
####################################


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 20 # milliseconds
    init(data)
    initScore(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1200,600)

