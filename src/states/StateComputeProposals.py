from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *


#sprawdzanie czy dokonano dealu 
class StateComputeProposals(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        print("Starting computing proposals, my name "+ self.fAgent.nameMy)



