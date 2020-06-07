from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy
from messages import StatesMessage


class StateComputeRisk(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        self.fAgent.logger.log_info("Starting computing risk")
        myUtility = 0.0        
        myUtility = float(self.fAgent.worst - self.fAgent.getMyCost(str(self.fAgent.currentSigma),self.fAgent.currentSigma))
        if myUtility == 0.0:
            myRisk = 1.0
        else:
            myRisk = 0.0;
            for co in self.fAgent.activeCoworkers:
                proposition = self.fAgent.matesProposals[co][len(self.fAgent.matesProposals[co])-1] 
                utility = float(self.fAgent.worst - self.fAgent.getMyCost(str(proposition),proposition))
                temp = (myUtility - utility)/myUtility
                if temp > myRisk:
                    myRisk = temp

        self.fAgent.logger.log_info(f"My risk equals {myRisk}")
        for co in self.fAgent.activeCoworkers:
            msg = StatesMessage(to=co, body=myRisk)
            msg.set_metadata("language", "float")
            await self.send(msg)

        # waiting for all responses from agents!!!
        waitingCoworkers = deepcopy(self.fAgent.activeCoworkers)     
        matesRisk = []
        while (len(waitingCoworkers)> 0 ):
            msg = await self.receive(timeout = 5)
            if msg is not None:
                sender = str(msg.sender)
                if msg.metadata["performative"] == "inform" and msg.metadata["language"] == "float":
                    waitingCoworkers.remove(sender)
                    matesRisk.append(float(msg.body))
                else:
                    self.fAgent.saveMessage(msg)

        #if my risk is the smalles -> I should concede!
        if myRisk <= min(matesRisk):
            self.fAgent.logger.log_info("I should concede")
            self.set_next_state(STATE_COMPUTE_CONCESSION)
        else:
            self.fAgent.logger.log_info("I should not concede")
            self.set_next_state(STATE_WAIT_FOR_NEXT_ROUND)