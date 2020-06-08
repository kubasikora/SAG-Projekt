from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy
import json
from messages import StatesMessage, InactiveMessage

class StateNotActive(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        if self.fAgent.optimal_result is None:
            self.fAgent.logger.log_warning(f"Aight, imma head out - disactivating with last cost {min(self.fAgent.allCalculatedCosts.values())}")
            for co in self.fAgent.activeCoworkers:
                msg = StatesMessage(to=co, body="False")
                msg.set_metadata("language", "boolean")
                await self.send(msg)

            # inform manager that agent went inactive
            result = {
                "last_sequence": self.fAgent.currentSigma,
                "cost": self.fAgent.getCostAll(str(self.fAgent.currentSigma))
            }
            message = InactiveMessage(to=self.fAgent.manager, body=json.dumps(result))
            await self.send(message)

        end = False
        while(end == False):
            resp = await self.receive(timeout=10)
            if resp is not None:
                sender = str(resp.sender)
                if resp.metadata["performative"] == "inform" and resp.body == "We have got it!":
                    end = True           
