from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from spade.message import Message
import random
from .metadata import *

MAX_COST = 10000000
#    to do stop agent if there are no sequences!!!
class StateComputeB0(State):

    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent


    #should add checking if we already now the price and should add saving the price of mates in agent!! 
    async def run(self):
        print("Starting computing b0, my name "+ self.fAgent.nameMy)
        B0prim = self.fAgent.B0prim
        stringSeq = str(B0prim[0])
        myCost = self.fAgent.getMyCost(stringSeq, B0prim[0])
        coworkersJID = self.fAgent.coworkers
        minCost = MAX_COST
        B0 = []
        for seq in B0prim:
            costSeq = myCost
            costAll = self.fAgent.getCostAll(str(seq))
            if costAll == -1:
                for cjid in coworkersJID:
                    msg=Message(to=cjid)
                    msg.set_metadata("conversation-id", "2")
                    msg.set_metadata("performative", "request")
                    msg.set_metadata("save", "True")
                    msg.body = str(seq)
                    await self.send(msg)
                    gotResponse = False
                    while gotResponse == False:
                        resp = await self.receive(timeout=5)
                        if resp is None:
                            print("Error") #probably we should raise exception or something !!!!!!!!!!!!!
                        else:
                            if resp.metadata["performative"] == "inform" and resp.metadata["language"] == "int" :
                                costSeq = costSeq + int(resp.body)
                                gotResponse = True
                            else:
                                self.fAgent.saveMessage(resp)
                self.fAgent.setCostAll(str(seq), costSeq)
            else:
                costSeq = costAll
            if costSeq < minCost:
                B0.clear()
                minCost = costSeq
            if costSeq <= minCost:
                B0.append(seq)

        sequence = random.choice(B0)
        if len(sequence) == 0:
            print("I am done")
            #ustaw stan na nieaktywny
        else:
            print("my seq "+self.fAgent.nameMy)
            print(sequence)
            B0.remove(sequence)
            self.fAgent.B0 = B0 
            self.fAgent.currentSigma = sequence
            #if self.self.fAgent.myWorstProposal
            if len(self.fAgent.myWorstProposal) == 0:
                self.fAgent.myWorstProposal = sequence
            elif self.fAgent.getMyCost(str(self.fAgent.myWorstProposal), self.fAgent.myWorstProposal) < myCost:
                self.fAgent.myWorstProposal = sequence
            self.set_next_state(STATE_PROPOSE)