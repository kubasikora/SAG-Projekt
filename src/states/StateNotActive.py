from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy
import json

class StateNotActive(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        if self.fAgent.optimal_result is None:
            self.fAgent.logger.log_warning(f"Aight, imma head out - disactivating with last cost {min(self.fAgent.allCalculatedCosts.values())}")
            for co in self.fAgent.activeCoworkers:
                msg = Message(to=co)
                msg.set_metadata("performative", "inform")
                msg.set_metadata("language","boolean" )
                msg.set_metadata("conversation-id", "1")
                msg.body = "False"
                await self.send(msg)

            # inform manager that agent went inactive
            message = Message(to=self.fAgent.manager)
            message.set_metadata("performative", "inform")
            message.set_metadata("conversation-id", "not-active")
            result = {
                "last_sequence": self.fAgent.currentSigma,
                "cost": self.fAgent.getCostAll(str(self.fAgent.currentSigma))
            }
            message.body = json.dumps(result)
            await self.send(message)

        end = False

        while(end == False):
            resp = await self.receive(timeout=10)
            if resp is not None:
                sender = str(resp.sender)
                if resp.metadata["performative"] == "inform" and resp.body == "We have got it!":
                    end = True           
