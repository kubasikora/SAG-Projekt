from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *


class StateComputeConcession(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        print("Waiting for coworkers, my name "+ self.fAgent.nameMy)