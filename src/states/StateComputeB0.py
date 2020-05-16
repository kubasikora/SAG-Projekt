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
        print("Starting computing b0, my name "+ self.agent.getName())
        B0prim = self.fAgent.getB0prim()
        stringSeq = str(B0prim[0])
        myCost = self.fAgent.getMyCost(stringSeq, B0prim[0])
        coworkersJID = self.fAgent.getCoworkers()
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
                    msg.body = str(seq)
                    await self.send(msg)
                    resp = await self.receive(timeout=15)
                    if resp is None:
                        print("Error") #probably we should raise exception or something !!!!!!!!!!!!!
                    if resp is not None:
                        costSeq = costSeq + int(resp.body)
                self.fAgent.setCostAll(str(seq), seq)
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
            print("my seq "+self.fAgent.getName())
            print(sequence)
            B0.remove(sequence)
            self.fAgent.setB0(B0) 
            self.fAgent.setCurrentSigma(sequence)
            self.set_next_state(STATE_PROPOSE)