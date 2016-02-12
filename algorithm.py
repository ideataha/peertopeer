#__author__ = 'ideataha'
import numpy,math,random,sys
#import matplotlib.pyplot,matplotlib
from random import randint

# numberofpeers=70
cycletorun=99999999

# if len(sys.argv) != 1:
#   numberofpeers=int(sys.argv[1])
#   cycletorun=int(sys.argv[2])

#number of trial for every parameters
numoftrial=100
numberofsupernode=14

#distance cannot be less than 1
#distance_between_supernode=10

#this will determine the area of the network
maxheightwidth=140
list_numberofpeers=[10,50,100,500,1000,10000,100000,1000000]
list_numberofsupernodes=[10,50,100,500,1000,10000,100000,1000000]
reread=True
verbose=False
printaverage=False
printallresnotavg=True
'''begin class to write in text file'''
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
    res=[]
    xxyy=[0.0,0.0,200.0,200.0]
    gpsaccuracy=6
    latsegments=[27,58,108,158,184,158,108,58,27,58,108,158,184]
    longsegments=[37,14,14,14,37,99,99,99,151,186,186,186,151]
    #latsegments=[27,58,108,158,184,158,108]
    #longsegments=[37,14,14,14,37,99,99]
    nodelist=[]
    supernodelist=[]
    POSITIVEINFINITY="z"
    NEGATIVEINFINITY="0"
    NULL="null"
    counter=0
    #latitude = x axis
    #longitude = y axis
    def compare(self,a,b):
        if a==b:
            return False
        if a==Global.NEGATIVEINFINITY or b==Global.POSITIVEINFINITY:
            return False
        if a==Global.POSITIVEINFINITY or b==Global.NEGATIVEINFINITY:
            return True
        aa=a.split("-")
        bb=b.split("-")
        ta=[]
        tb=[]
        del ta[:]
        del tb[:]
        for i,aaa in enumerate(aa):
            if i!=0:
                if len(aaa)!=10:
                    temp=10-len(aaa)
                    for z in range(temp):
                        aaa+="0"
            ta.append(int(aaa))
        for i,bbb in enumerate(bb):
            if i!=0:
                if len(bbb)!=10:
                    temp=10-len(bbb)
                    for z in range(temp):
                        bbb+="0"
            tb.append(int(bbb))
        for i in range(len(ta)):
            if ta[i]<tb[i]:
                return False
            if ta[i]>tb[i]:
                return True
    def genlatlong(num):
        del Global.latsegments[:]
        del Global.longsegments[:]
        distance_between_supernode=num*1.0/maxheightwidth
        for i in range(num):
            Global.longsegments.append(i*distance_between_supernode)
            Global.latsegments.append(i*distance_between_supernode)

    def dist(x1,x2,y1,y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def createlong(self):
        return round(random.uniform(Global.longsegments[0],Global.longsegments[-1]),Global.gpsaccuracy)

    def createlat(self):
        return round(random.uniform(Global.latsegments[0],Global.latsegments[-1]),Global.gpsaccuracy)

    '''def createlatflat(self,lmin,lmax):
        return round(random.uniform(lmin,lmax),Global.gpsaccuracy)'''
    def createid(self):
        return random.randint(1,9999999999)
    def generate_nodes_supernodes(self,sn,n):
        Global.genlatlong(sn)
        del Global.nodelist[:]
        del Global.supernodelist[:]
        temp=0

        while temp < sn:
            Global.supernodelist.append(Node(True,Global.createid(Global),Global.longsegments[temp],Global.latsegments[temp]))
            Global.nodelist.append(Global.supernodelist[-1])
            if temp != 0:
                Global.supernodelist[-1].left = Global.supernodelist[-2].id
                Global.supernodelist[-2].right = Global.supernodelist[-1].id
            temp=temp+1
        for i in range (n):
            #below for in 2D with random nodes
            Global.nodelist.append(Node(False,Global.createid(Global),Global.createlat(Global),Global.createlong(Global)))
            #create diagonal lienar supernode in 2D area
            #Global.nodelist.append(Node(False,Global.createid(Global),i*10,i*10))
            #below for in 1D 
            #Global.nodelist.append(Node(False,Global.createid(Global),Global.createlatflat(Global,0,Global.latsegments[-1]),0))

    def iteratelinearizednode(self,tnode,newid,oldid,trialnumber,numofnode,numofsupernode,cyclenumber):
        if verbose:
            print("list of linearized peers")
        temp=0
        while temp < len(Global.nodelist):
            temp+=1
            iss = ""
            if tnode.issupernode:
                iss="\t(s)\t"
            extratab=""
            if tnode.left == Global.NEGATIVEINFINITY:
                extratab="\t"
            extratab2=""
            if tnode.right == Global.POSITIVEINFINITY:
                extratab2="\t\t"
            if verbose:
                print("%d : \t%s \t%s<- %s -> \t%s%s %s - %d messages" % (temp,tnode.left,extratab,tnode.id,tnode.right,extratab2, iss, len(tnode.messagebuffer)))
            tnode.isarranged=True
            for node in Global.nodelist:
                if node.id == tnode.right:
                    tnode=node
                    break

            if Global.compare(Global,newid,oldid):
                oldid=newid
                newid=tnode.id
                if temp == len(Global.nodelist):
                    if verbose:
                        print ("number of node: %d  -  trial number:%d  -  number of cycle: %d" %(numofnode,trialnumber,cyclenumber))
                    Global.res.append(tempo)
                    if printallresnotavg:
                        print(numofsupernode,",",numofnode,",",cyclenumber)
                    return False
            else:
                break
        return True


    def findunlinearizednode():
        print("\n\nlist of unlinearized peers for cycle: %d. All nodes is linearized if there is no single node down here" % tempo)
        counter = 1
        for nod in Global.nodelist:
            if nod.isarranged == False:
                iss = ""
                if nod.issupernode:
                    iss="\t(s)\t"
                print("%d  -  %s <>  %s  <>  %s  --> %d messages %s" % (counter, nod.left,nod.id,nod.right, len(nod.messagebuffer), iss))
                counter = counter+1
            
    def printresult(self,cycletorun,numberofnode,numberofsupernode):
        meantxt=""
        if len(Global.res)==0:
            meantxt="the topology fail to stabilize in number of cycle less than %d" % cycletorun
        else:
            meantxt="the mean is %f" % numpy.mean(Global.res)
        if printaverage:
            print("for node=",numberofnode,", supernode=",numberofsupernode,meantxt)
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
            if msg.message == self.right or msg.message == self.left or msg.message == self.id or msg.message == Global.POSITIVEINFINITY or msg.message == Global.NEGATIVEINFINITY:
                self.readmessage()
                return
            
            #if msg.message < self.left:
            if Global.compare(Global,self.left,msg.message):
                self.sendmessage(1,msg.message,self.left)
                return

            #if msg.message > self.right:
            if Global.compare(Global,msg.message,self.right):
                self.sendmessage(1,msg.message,self.right)
                return

            #if msg.message > self.left and msg.message < self.id:
            if Global.compare(Global,msg.message,self.left) and Global.compare(Global,self.id,msg.message):
                self.changeneighbour(True,msg.message)
                return
                    
            #if msg.message < self.right and msg.message > self.id:
            if Global.compare(Global,self.right,msg.message) and Global.compare(Global,msg.message,self.id):
                self.changeneighbour(False,msg.message)
                return

            self.readmessage()

        else:
            self.readmessage()



    def changeneighbour(self,isleft,neighbour):
        if isleft:
            self.sendmessage(1,self.left,neighbour)
            if self.left != Global.NEGATIVEINFINITY:
                self.sendmessage(1,neighbour,self.left)
            self.left=neighbour
        else:
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
                #if node.id < self.id:
                if Global.compare(Global,self.id,node.id):
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
            #print("check whether left neighbor is correct")
        if self.left != Global.NEGATIVEINFINITY and self.timeoutleft:
            self.sendmessage(1,self.id,self.left)
            #self.timeoutleft=False
            #print("check whether right neighbor is correct if available")
        if self.right != Global.POSITIVEINFINITY and self.timeoutright:
            self.sendmessage(1,self.id,self.right)
            #self.timeoutright=False

'''end node class'''


numberofsupernode=list_numberofsupernodes[1]
for n_p in list_numberofpeers:
    del Global.res[:]
    for trial in range(numoftrial):
        Global.generate_nodes_supernodes(Global,numberofsupernode,n_p)
        tempo=0
        fflag=True
        while tempo < cycletorun and fflag:
            tempo+=1
            if verbose:
                print("\n\n\n\n\n\nCycle # : %d" % tempo)
            tnode=Global.nodelist[0]
            for node in Global.nodelist:
                if node.id < tnode.id:
                    tnode=node

            fflag=Global.iteratelinearizednode(Global,tnode,tnode.id,Global.NEGATIVEINFINITY,trial,n_p,numberofsupernode,tempo)
            if verbose:
                Global.findunlinearizednode()

            for node in Global.nodelist:
                node.run()
    Global.printresult(Global,cycletorun,n_p,numberofsupernode)
        
    
numberofnode=list_numberofpeers[1]
for n_s in list_numberofsupernodes:
    del Global.res[:]
    for trial in range(numoftrial):
        Global.generate_nodes_supernodes(Global,n_s,numberofnode)
        tempo=0
        fflag=True
        while tempo < cycletorun and fflag:
            tempo+=1
            if verbose:
                print("\n\n\n\n\n\nCycle # : %d" % tempo)
            tnode=Global.nodelist[0]
            for node in Global.nodelist:
                if node.id < tnode.id:
                    tnode=node

            fflag=Global.iteratelinearizednode(Global,tnode,tnode.id,Global.NEGATIVEINFINITY,trial,numberofnode,n_s,tempo)
            if verbose:
                Global.findunlinearizednode()
            for node in Global.nodelist:
                node.run()
    Global.printresult(Global,cycletorun,numberofnode,n_s)

#use the original
sys.stdout = original
#print("This won't appear on file")  # Only on stdout
f.close()
