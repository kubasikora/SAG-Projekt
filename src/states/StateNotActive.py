from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy


class StateNotActive(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):

        print("Disactivating, my name "+ self.fAgent.nameMy)
        print(min(self.fAgent.allCalculatedCosts.values()))
        for co in self.fAgent.activeCoworkers:
            msg = Message(to=co)
            msg.set_metadata("performative", "inform")
            msg.set_metadata("language","boolean" )
            msg.set_metadata("conversation-id", "1")
            msg.body = "False"
            await self.send(msg)

        end = False

        while(end == False):
            resp = await self.receive(timeout=10)
            if resp is not None:
                sender = str(resp.sender)
                if resp.metadata["performative"] == "inform" and resp.body == "We have got it!":
                    end = True           
