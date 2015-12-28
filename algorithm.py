#__author__ = 'ideataha'
import random
import math
import sys
from random import randint

numberofpeers=70
cycletorun=1000

if len(sys.argv) != 1:
	numberofpeers=int(sys.argv[1])
	cycletorun=int(sys.argv[2])

reread=True


'''begin class to write in text fiel'''
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()


'''end class to write in text field'''
f = open('algorithm.txt', 'w')
original = sys.stdout
sys.stdout = Tee(sys.stdout, f)
#print("test")  # This will go to stdout and the file out.txt


'''begin global class'''
class Global:
    xxyy=[0.0,0.0,200.0,200.0]
    gpsaccuracy=6
    #latsegments=[27,58,108,158,184,158,108,58,27,58,108,158,184]
    #longsegments=[37,14,14,14,37,99,99,99,151,186,186,186,151]
    latsegments=[27,58,108,158,184,158,108]
    longsegments=[37,14,14,14,37,99,99]
    nodelist=[]
    supernodelist=[]
    POSITIVEINFINITY="z"
    NEGATIVEINFINITY="0"
    NULL="null"
    counter=0
    #latitude = x axis
    #longitude = y axis
    def dist(x1,x2,y1,y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    def createlong(self):
        return round(random.uniform(Global.xxyy[1],Global.xxyy[3]),Global.gpsaccuracy)
    def createlat(self):
        return round(random.uniform(Global.xxyy[0],Global.xxyy[2]),Global.gpsaccuracy)
    def createid(self):
        return random.randint(1,9999999999)

    def iterate(self):
        print("done")
'''end global class'''


'''begin messsage class'''
class Message(object):
    def __init__(self,code,sender,message):
        self.code=code
        #self.sender=sender
        self.message=message
'''end messsage class'''


'''begin node class'''
class Node(object):
    test=0
    def sendmessage(self,code,message,receiver):
        for node in Global.nodelist:
            if node.id == receiver:
                node.messagebuffer.append(Message(code,self.id,message))
                break


    def readmessage(self):
        if len(self.messagebuffer) == 0:
            return
        index=random.randint(0,(len(self.messagebuffer)-1))
        msg=self.messagebuffer[index]
        del self.messagebuffer[index]

        if msg.code == 1:
            if msg.message == self.right or msg.message == self.left:
                self.readmessage()
                return
            
            if msg.message < self.left:
                self.sendmessage(1,msg.message,self.left)
                return

            if msg.message > self.right:
                self.sendmessage(1,msg.message,self.right)
                return

            if msg.message > self.left and msg.message < self.id:
                self.changeneighbour(msg.message)
                return
                    
            if msg.message < self.right and msg.message > self.id:
                self.changeneighbour(msg.message)
                return

        else:
            self.readmessage()



    def changeneighbour(self,neighbour):
        if neighbour<self.id:
            if neighbour != Global.NEGATIVEINFINITY:
                self.sendmessage(1,self.left,neighbour)
            if self.left != Global.NEGATIVEINFINITY:
                self.sendmessage(1,neighbour,self.left)
            self.left=neighbour
        elif neighbour>self.id:
            if neighbour != Global.POSITIVEINFINITY:
                self.sendmessage(1,self.right,neighbour)
            if self.right != Global.POSITIVEINFINITY:
                self.sendmessage(2,neighbour,self.right)
            self.right=neighbour


    def __init__(self,issp,id, long,lat):
        self.id = Global.NULL
        self.reread = True
        self.timeoutleft = True
        self.timeoutright = True
        self.segment=0
        self.originalid=0
        self.isdead = False
        self.issupernode = False
        self.right = Global.POSITIVEINFINITY
        self.left = Global.NEGATIVEINFINITY
        self.lat = 3.1
        self.long = 101.1
        self.messagebuffer=[]
        self.long=long
        self.lat=lat
        self.originalid=id
        self.issupernode=issp
        self.isarranged=False #just to check whether the node is already queued
        self.setsegment()
        

    def setsegment(self):
        distance=9999999999999999.9
        index=0
        while index < len(Global.latsegments):
            newdistance=Global.dist(self.lat,Global.latsegments[index],self.long,Global.longsegments[index])
            if newdistance < distance:
                distance=newdistance
                self.segment=index
            index = index+1
        self.id="%d-%d" % (self.segment,self.originalid)
        for node in Global.supernodelist:
            if node.segment == self.segment:
                if node.id < self.id:
                    self.left=node.id
                    self.right=Global.POSITIVEINFINITY
                else:
                    self.right=node.id
                    self.left=Global.NEGATIVEINFINITY
                break

    def run(self):
        if len(self.messagebuffer) != 0:
            self.readmessage()
        while self.reread and len(self.messagebuffer) != 0:
            self.readmessage()
            #print("check whether left neighbour is correct")
        if self.left != Global.NEGATIVEINFINITY and self.timeoutleft:
            self.sendmessage(1,self.id,self.left)
            #self.timeoutleft=False
            #print("check whether right neighbour is correct if available")
        if self.right != Global.POSITIVEINFINITY and self.timeoutright:
            self.sendmessage(1,self.id,self.right)
            #self.timeoutright=False

'''end node class'''



temp=0
while temp < len(Global.latsegments):
    Global.supernodelist.append(Node(True,Global.createid(Global),Global.longsegments[temp],Global.latsegments[temp]))
    Global.nodelist.append(Global.supernodelist[-1])
    if temp != 0:
        Global.supernodelist[-1].left = Global.supernodelist[-2].id
        Global.supernodelist[-2].right = Global.supernodelist[-1].id

    temp=temp+1



for i in range(numberofpeers):
    Global.nodelist.append(Node(False,Global.createid(Global),Global.createlat(Global),Global.createlong(Global)))

tempo=0
fflag=True
while tempo < cycletorun and fflag:
    tempo=tempo+1
    print("\n\n\n\n\n\nCycle # : %d" % tempo)
    for node in Global.nodelist:
        node.run()

    
    tnode=Global.nodelist[0]
    for node in Global.nodelist:
        if node.id < tnode.id:
            tnode=node
    temp=0
    newid=tnode.id
    
    oldid=Global.NEGATIVEINFINITY
    for n in Global.nodelist:
        n.isarranged=False

    print("list of lineared peers")
    while temp < len(Global.nodelist):
        temp=temp+1
        iss = ""
        if tnode.issupernode:
            iss="\t(s)\t"

        extratab=""
        if tnode.left == Global.NEGATIVEINFINITY:
            extratab="\t"
        extratab2=""
        if tnode.right == Global.POSITIVEINFINITY:
            extratab2="\t\t"
        print("%d : \t%s \t%s<- %s -> \t%s%s %s - %d messages" % (temp,tnode.left,extratab,tnode.id,tnode.right,extratab2, iss, len(tnode.messagebuffer)))

        tnode.isarranged=True

        
        for node in Global.nodelist:
            if node.id == tnode.right:
                tnode=node
                break
        if newid > oldid:
            oldid=newid
            newid=tnode.id
            if temp == len(Global.nodelist):
                fflag=False
        else:
            break

    print("\n\nlist of unlinearized peers for cycle: %d" % tempo)
    counter = 1
    for nod in Global.nodelist:
        if nod.isarranged == False:
            print("%d  -  %s <>  %s  <>  %s" % (counter, nod.left,nod.id,nod.right))
            counter = counter+1



#use the original
sys.stdout = original
#print("This won't appear on file")  # Only on stdout
f.close()