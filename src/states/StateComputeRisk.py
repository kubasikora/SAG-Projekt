from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *


class StateComputeRisk(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        print("Starting computing risk, my name "+ self.fAgent.nameMy)
        myUtility = 0.0        
        myUtility = float(self.fAgent.worst - self.fAgent.getMyCost(str(self.fAgent.currentSigma),self.fAgent.currentSigma))
        if myUtility == 0.0:
            risk = 1.0
        else:
            risk = 0.0;
            for co in self.fAgent.activeCoworkers:
                proposition = self.fAgent.matesProposals[co][len(self.fAgent.matesProposals[co])-1] 
                utility = float(self.fAgent.worst - self.fAgent.getMyCost(str(proposition),proposition))
                temp = (myUtility - utility)/myUtility
                if temp > risk:
                    risk = temp
        print("my risk! "+str(risk))
