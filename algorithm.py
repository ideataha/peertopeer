#__author__ = 'ideataha'
from sortedcontainers import SortedList, SortedSet, SortedDict,SortedListWithKey
from operator import itemgetter, attrgetter
import numpy,math,random,sys
from random import randint
from datetime import datetime

# numberofpeers=70
cycletorun=99999999

#uncomment this to use arguments in terminal
# if len(sys.argv) != 1:
#   numberofpeers=int(sys.argv[1])
#   cycletorun=int(sys.argv[2])

#number of trial for every parameters
numoftrial=10
#numberofsupernode=14

#this will determine the 2D plane area of the network
maxheightwidth=140

#list_numberofpeers=[10,20,30,40,50,60,70,80,90,100,150,200,250,300,350,400,450,500,550,600,700,800,900,1000,1000000]
list_numberofpeers=[]
i=6000
while i < 8000:
    list_numberofpeers.append(i)
    i+=100
#list_numberofsupernodes=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]
list_numberofsupernodes=[]
i=2000
while i <= 2000:
    list_numberofsupernodes.append(i)
    i+=10
verbose=False
printaverage=False #print average cycle needed only for every test case
printallresnotavg=True #print number of cycle needed for every test case
printeverycycle=False #print something is a cycle is passed
if_message_read_in_any_node=False #print dot (.) if any node read any message
read_all_message_once_run=False #every nodes should read all messages in their queue everytime they run



# test - to be deleted

list_numberofpeers=[10,16,16]
list_numberofsupernodes=[12,13,15,16,18]
verbose=True

# finish - test








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
    multipurposecounter=0 #just a global counter to be used for debugging at anywhere
    res=[]
    xxyy=[0.0,0.0,200.0,200.0]
    gpsaccuracy=6
    latsegments=[27,58,108,158,184,158,108,58,27,58,108,158,184]
    longsegments=[37,14,14,14,37,99,99,99,151,186,186,186,151]

    nodesortedlist = SortedListWithKey(key=lambda Node: Node.id)
    #supernodesortedlist = SortedListWithKey(key=lambda Node: Node.id)
    #POSITIVEINFINITY="z"
    #NEGATIVEINFINITY="-"
    POSITIVEINFINITY=999999999999999999999999999999999999999
    NEGATIVEINFINITY = -999999999
    #NULL="null"
    NULL = -1.1
    counter=0
    latestimmutableid=10001

    ''' define method is to compare between 2 mutable ID. normal comparison wont work in some cases. by the way, this is not the cause of delay'''
    def compare(self,a,b):
        return a > b
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



    ''' method to generate longitude and latitude of supernode'''
    def genlatlong(num):
        del Global.latsegments[:]
        del Global.longsegments[:]
        #distance_between_supernode=num*1.0/maxheightwidth
        for i in range(num):
            #Global.longsegments.append(i*distance_between_supernode)
            #Global.latsegments.append(i*distance_between_supernode)
            #print(i)
            Global.longsegments.append(i)
            Global.latsegments.append(i)

    ''' method to find distance between two points in 2-D plane'''
    def dist(x1,x2,y1,y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    '''generate random longitude'''
    def createlong(self):
        return round(random.uniform(Global.longsegments[0],Global.longsegments[-1]),Global.gpsaccuracy)
    '''generate random latitude'''
    def createlat(self):
        return round(random.uniform(Global.latsegments[0],Global.latsegments[-1]),Global.gpsaccuracy)

    '''generate random ID'''
    def createid(self):
        Global.latestimmutableid+=1
        return Global.latestimmutableid
        #return random.randint(1,99999999999999999999999999999999999999)

    ''' generate random node and supernode and add them into node and supernodelist'''
    def generate_nodes_supernodes(self,sn,n):
        Global.genlatlong(sn)
        Global.nodesortedlist.clear()
        #Global.supernodesortedlist.clear()
        temp=0

        while temp < sn:
            #Global.supernodesortedlist.add(Node(True,Global.createid(Global),Global.longsegments[temp],Global.latsegments[temp]))
            Global.nodesortedlist.add(Node(True,Global.createid(Global),Global.longsegments[temp],Global.latsegments[temp]))
            #Global.nodesortedlist.add(Global.supernodesortedlist[-1])
            #print(Global.nodesortedlist[-1].lat,"  -  ",Global.nodesortedlist[-1].long)
            if temp != 0:
                #Global.supernodesortedlist[-1].left=Global.supernodesortedlist[-2].id
                #Global.supernodesortedlist[-2].right=Global.supernodesortedlist[-1].id
                Global.nodesortedlist[-1].left=Global.nodesortedlist[-2].id
                Global.nodesortedlist[-2].right=Global.nodesortedlist[-1].id
            temp=temp+1
        for i in range (n):
            Global.nodesortedlist.add(Node(False,Global.createid(Global),Global.createlat(Global),Global.createlong(Global)))
            
    ''' iterate nodes (including supernode) from negative infinity to positive infinity. if found positive infinity earlier or longer than expected, means not linearized yet'''
    def iteratelinearizednode(self,tnode,newid,oldid,trialnumber,numofnode,numofsupernode,cyclenumber):
        if printeverycycle:
            print('a cycle')
        if verbose:
            print("list of linearized peers")
        temp=0
        while temp < len(Global.nodesortedlist):
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
                print("%d : \t%f \t%s<- %f -> \t%f%s %s - %d messages" % (temp,tnode.left,extratab,tnode.id,tnode.right,extratab2, iss, len(tnode.messagebuffer)))
                #print("%d : \t%s \t%s<- %s -> \t%s%s %s - %d messages" % (temp,tnode.left,extratab,tnode.id,tnode.right,extratab2, iss, len(tnode.messagebuffer)))
            tnode.isarranged=True
            for node in Global.nodesortedlist:
                if node.id == tnode.right:
                    tnode=node
                    break

            if Global.compare(Global,newid,oldid):
                oldid=newid
                newid=tnode.id
                if temp == len(Global.nodesortedlist):
                    if verbose:
                        print ("number of node: %d  -  trial number:%d  -  number of cycle: %d" %(numofnode,trialnumber,cyclenumber))
                    Global.res.append(tempo)
                    if printallresnotavg:
                        #Global.multipurposecounter+=1
                        print(numofsupernode,",",numofnode,",",cyclenumber)
                    return False
            else:
                break
        return True


    '''this method is not called if not using verbose mode. this is just to keep track which node is still not flagged as linearized yet'''
    def findunlinearizednode():
        print("\n\nlist of unlinearized peers for cycle: %d. All nodes is linearized if there is no single node down here" % tempo)
        counter = 1
        for nod in Global.nodesortedlist:
            if nod.isarranged == False:
                iss = ""
                if nod.issupernode:
                    iss="\t(s)\t"
                print("%d  -  %f <>  %f  <>  %f  --> %d messages %s" % (counter, nod.left,nod.id,nod.right, len(nod.messagebuffer), iss))
                #print("%d  -  %s <>  %s  <>  %s  --> %d messages %s" % (counter, nod.left,nod.id,nod.right, len(nod.messagebuffer), iss))
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
    '''insert a message into another node's message queue'''
    def sendmessage(self,code,message,receiver):
        Global.nodesortedlist[Global.nodesortedlist.bisect_key(receiver)-1].messagebuffer.add(Message(code,self.id,message))

    
    def readmessage(self):
        if if_message_read_in_any_node:
            print('.',end='')
        if len(self.messagebuffer) == 0:
            return
        '''index=random.randint(0,(len(self.messagebuffer)-1))
        msg=self.messagebuffer[index]
        del self.messagebuffer[index]'''
        msg=self.messagebuffer.pop(0)

        if msg.code == 1:
            if msg.message == self.right or msg.message == self.left or msg.message == self.id or msg.message == Global.POSITIVEINFINITY or msg.message == Global.NEGATIVEINFINITY:
                return True
            
            #if msg.message < self.left:
            if Global.compare(Global,self.left,msg.message):
                self.sendmessage(1,msg.message,self.left)


            #if msg.message > self.right:
            elif Global.compare(Global,msg.message,self.right):
                self.sendmessage(1,msg.message,self.right)

            #if msg.message > self.left and msg.message < self.id:
            elif Global.compare(Global,msg.message,self.left) and Global.compare(Global,self.id,msg.message):
                self.changeneighbour(True,msg.message)

                    
            #if msg.message < self.right and msg.message > self.id:
            elif Global.compare(Global,self.right,msg.message) and Global.compare(Global,msg.message,self.id):
                self.changeneighbour(False,msg.message)

            return read_all_message_once_run

        return False
        '''else:
            self.readmessage()'''



    def changeneighbour(self,isleft,neighbour):
        if isleft:
            self.sendmessage(1,self.left,neighbour)
            if self.left != Global.NEGATIVEINFINITY:
                self.sendmessage(1,neighbour,self.left)
            self.left=neighbour
        else:
            self.sendmessage(1,self.right,neighbour)
            if self.right != Global.POSITIVEINFINITY:
                self.sendmessage(1,neighbour,self.right)
            self.right=neighbour


    def __init__(self,issp,id, long,lat):
        self.id = Global.NULL
        #self.reread = True
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
        self.messagebuffer = SortedListWithKey(key=lambda Message: Message.message)
        self.long=long
        self.lat=lat
        self.originalid=id
        self.issupernode=issp
        self.isarranged=False #just to check whether the node is already queued
        self.setsegment()
        
    '''assign segment to node'''
    def setsegment(self):
        distance=9999999999999999.9
        index=0
        while index < len(Global.latsegments):
            newdistance=Global.dist(self.lat,Global.latsegments[index],self.long,Global.longsegments[index])
            if newdistance < distance:
                distance=newdistance
                self.segment=index
            index = index+1
        #self.id="%d-%d" % (self.segment,self.originalid)
        self.id=float("%d.%d" % (self.segment,self.originalid))

        #for node in Global.supernodesortedlist:
        for node in Global.nodesortedlist:
            if node.issupernode == True and node.segment == self.segment:

                if Global.compare(Global,self.id,node.id):
                    self.left=node.id
                    self.right=Global.POSITIVEINFINITY
                else:
                    self.right=node.id
                    self.left=Global.NEGATIVEINFINITY
                break

    def run(self,cycle):
        need_to_reread=False
        if len(self.messagebuffer) != 0:
            need_to_reread=self.readmessage()
        #flg=False
        while need_to_reread and len(self.messagebuffer) != 0:
            #flg=True
            self.readmessage()

        '''if flg or False:
            return'''
        '''if cycle % 5 == 0:
            return'''
        '''if self.left != Global.NEGATIVEINFINITY and self.right != Global.POSITIVEINFINITY:
            return'''
        if self.left != Global.NEGATIVEINFINITY and self.timeoutleft:
            self.sendmessage(1,self.id,self.left)

        if self.right != Global.POSITIVEINFINITY and self.timeoutright:
            self.sendmessage(1,self.id,self.right)

'''end node class'''



'''The Test Case---------------------------------------------------'''


#numberofsupernode=list_numberofsupernodes[1]
numberofsupernode=10
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

            tnode=Global.nodesortedlist[0]

            for node in Global.nodesortedlist:
                if node.id < tnode.id:
                    tnode=node

            fflag=Global.iteratelinearizednode(Global,tnode,tnode.id,Global.NEGATIVEINFINITY,trial,n_p,numberofsupernode,tempo)
            if verbose:
                Global.findunlinearizednode()


            for node in Global.nodesortedlist:
                node.run(tempo)
    Global.printresult(Global,cycletorun,n_p,numberofsupernode)

'''case #2 - Vary number of supernode, fix number of node'''
'''
#numberofnode=list_numberofpeers[1]
numberofnode=100
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

            tnode=Global.nodesortedlist[0]

            for node in Global.nodesortedlist:
                if node.id < tnode.id:
                    tnode=node

            fflag=Global.iteratelinearizednode(Global,tnode,tnode.id,Global.NEGATIVEINFINITY,trial,numberofnode,n_s,tempo)
            if verbose:
                Global.findunlinearizednode()

            for node in Global.nodesortedlist:
                node.run(tempo)
                #print(node.long," - ",node.lat)
            #break #buang ni nnt
        #break #buang ni nnt
    Global.printresult(Global,cycletorun,numberofnode,n_s)
    #break #buang ni nnt
'''


#use the original input output (not printing into textfile)
sys.stdout = original
#print("This won't appear on file")  # Only on stdout
f.close()
