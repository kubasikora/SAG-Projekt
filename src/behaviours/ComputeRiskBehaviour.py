from spade.behaviour import CyclicBehaviour
from agents import FactoryAgent
from spade.message import Message


def parseMessage(string): # the format of the string [[[],[], ..], 'break', [[],[],...]]
    string = string.replace(" ", "")
    lists = string.split("break")
    toReturn = []
    for l in lists:
        l = l.replace("'", "")
        l = l.replace("]", "")
        l = l.replace("[", "")
        if(l[0] == ","):
            l = l[1:]
        nums = l.split(",")
        sigma = []
        for n in nums:
            sigma.append(int(n))
        toReturn.append(sigma)
    return toReturn


class ComputeRiskBehaviour(CyclicBehaviour):
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    def computeRisk(self, my, other):
        myUtility = float(self.fAgent.worst - self.fAgent.getMyCost(str(my),my))
        if myUtility == 0.0:
            return 1.0
        utility = float(self.fAgent.worst - self.fAgent.getMyCost(str(other),other))
        risk = (myUtility - utility)/myUtility
        return risk

    async def run(self):
        msg = await self.receive(timeout = 5)
        if msg is not None:
            #print("Got a message!")
            if(msg.body is not ""):
                sigmas = parseMessage(msg.body) #sigmas[0] - other sigmas[1] - my
                risk = self.computeRisk(sigmas[1], sigmas[0])
                msgResp = Message(to=str(msg.sender))     # Instantiate the message
                msgResp.set_metadata("performative", "inform")
                msgResp.set_metadata("language","float" )
                msgResp.set_metadata("conversation-id", "1")
                msgResp.body = str(risk)
                await self.send(msgResp)

    async def on_end(self):
        await self.agent.stop()