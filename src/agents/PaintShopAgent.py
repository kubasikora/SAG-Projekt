import time
from spade.agent import Agent
from spade.message import Message 
from spade.behaviour import State, FSMBehaviour
import json
from Cars import *

STATE_WAIT_FOR_TASK = "STATE_WAIT_FOR_TASK"
STATE_INIT = "STATE_INIT"
STATE_PROPOSE = "STATE_PROPOSE"
STATE_RISK = "STATE_RISK"
STATE_NEW_PROPOSITION = "STATE_NEW_PROPOSITION"
STATE_WAIT_FOR_REST = "STATE_WAIT_FOR_REST"
STATE_INACTIVE = "STATE_INACTIVE"



def getStartMsgContent(msg):
    msgType = msg.get_metadata("performative")
    if msgType == "request" : #probably more checks should be added (if it is good msg)
        res = json.loads(msgBody) # message should be dictonary with info about number of cars from each time which means that it should contain pairs key (which is index from 0 to 26) value (int >= 0)
        #probably more checking if it ok
        return res
    else:
        return None

class PaintShopAgent(Agent):

    self.costOne = 5
    self.costChange = 6

    def subscribeAll(jidList):
        for jid in jidList:
            self.presence.subscribe(jid)

    def on_subscribe(self, jid):
        self.presence.approve(jid)

    def calculateWorstCost(sameIndex, toProd): #sameIndex=[[], [], []] toProd={0:x, 1:y, ..., 26:z} x, y, z >=0
        #algorytm zwracajacy najgorsyz koszr

    class StateWaitForTask(State):  
        async def run(self):
            print("Starting new task ")
            self.owner.myProposedSolution = []
            self.owner.assemProposedSolution = []
            self.owner.weldProposedSolution = []
            msg = await self.receive() # wait for a message for 10 seconds
            if msg:
                #print("Message {} received with content: {}".format(self.counter, msg.body))
                #self.counter += 1
                #convert msg to check if it is ok
                self.owner.toProduce = getStartMsgContent(msg)
                if self.owner.toProduce is not None:
                    self.presence.set_presence(PresenceShow.AWAY, "init" )
                    self.set_next_state(STATE_INIT)
                else:
                    self.set_next_state(STATE_WAIT_FOR_TASK)

                
    class StateInit(State):
        async def run(self):
            print("initiaising")
            self.owner.sameIndex = getSameIndexesColors
            self.worst = calculateWorstCost(self.owner.sameIndex, self.owner.toProduce)
            
            

    async def on_end(self):
        await self.agent.stop()



    async def setup(self): 
        #to do write setup!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

"""
    1. Kazdy agent musi miec kilka zachowan 
        -> sprawdzajace czy pozostali zyja
        -> oczekujace na nowe zlecenie
        -> maszyna stanow obliczania
"""