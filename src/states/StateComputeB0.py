from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from spade.message import Message
from messages import CostMessage
import random
from .metadata import *

MAX_COST = 10000000
MAX_TIMES = 3
#    to do stop agent if there are no sequences!!!
class StateComputeB0(State):
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    #should add checking if we already now the price and should add saving the price of mates in agent!! 
    async def run(self):
        self.fAgent.logger.log_info(f"Starting computing b0")
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
                    counter = 0
                    msg=CostMessage(to=cjid, body=seq)
                    await self.send(msg)

                    gotResponse = False
                    while gotResponse == False:
                        resp = await self.receive(timeout=5)
                        if resp is None:                            
                            counter = counter + 1
                            if counter < MAX_TIMES:
                                self.fAgent.logger.log_error("Error in B0, retrying") 
                                msg=CostMessage(to=cjid, body=seq)
                            else:
                                self.fAgent.logger.log_error("Error in B0, we have to raise exception!!!") 
                                # probably we should raise exception or something !!!!!!!!!!!!!
                        else:
                            if resp.metadata["performative"] == "inform" and resp.metadata["language"] == "int" and str(resp.sender) == cjid:
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
            self.fAgent.logger.log_warning("I am done")
            self.set_next_state(STATE_NOT_ACTIVE)
        else:
            self.fAgent.logger.log_success(f"My seq {sequence}")
            B0.remove(sequence)
            self.fAgent.B0 = B0 
            self.fAgent.currentSigma = sequence

            if len(self.fAgent.myWorstProposal) == 0:
                self.fAgent.myWorstProposal = sequence

            elif self.fAgent.getMyCost(str(self.fAgent.myWorstProposal), self.fAgent.myWorstProposal) < myCost:
                self.fAgent.myWorstProposal = sequence
            
            self.set_next_state(STATE_PROPOSE)