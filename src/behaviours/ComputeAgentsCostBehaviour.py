from spade.behaviour import CyclicBehaviour
from agents import FactoryAgent
from spade.message import Message
from messages import StatesMessage

class ComputeAgentsCostBehaviour(CyclicBehaviour):
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    def parseMessage(self, body):
        without = body.replace("[", "")
        without = without.replace("]", "")
        without = without.replace(" ", "")
        nums = without.split(",")
        toReturn = []
        for num in nums:
            toReturn.append(int(num))
        return toReturn  

    async def run(self):
        msg = await self.receive(timeout = 5)
        if msg is not None:
            if msg.body is not "":
                sigma = self.parseMessage(msg.body)
                cost = self.fAgent.getMyCost(msg.body, sigma)

                if msg.metadata["save"] == "True":
                    self.fAgent.saveMatesBest(str(msg.sender), sigma)
                
                msgResp = StatesMessage(to=msg.sender, body=cost)
                msgResp.set_metadata("language", "int")
                await self.send(msgResp)
