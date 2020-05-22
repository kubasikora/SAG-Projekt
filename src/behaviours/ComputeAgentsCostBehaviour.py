from spade.behaviour import CyclicBehaviour
from agents import FactoryAgent
from spade.message import Message

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
            #print("Got a message!")
            if(msg.body is not ""):
                sigma = self.parseMessage(msg.body)
                cost = self.fAgent.getMyCost(msg.body, sigma)
                msgResp = Message(to=str(msg.sender))     # Instantiate the message
                msgResp.set_metadata("performative", "inform")
                msgResp.set_metadata("language","int" )
                msgResp.set_metadata("conversation-id", "1")
                msgResp.body = str(cost)
                await self.send(msgResp)

    async def on_end(self):
        await self.agent.stop()