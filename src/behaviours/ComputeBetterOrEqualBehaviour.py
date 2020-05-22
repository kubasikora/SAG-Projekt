from spade.behaviour import CyclicBehaviour
from agents import FactoryAgent
from spade.message import Message
"""
    Zachowanie do wyznaczania zbioru sekwencji, ktore dla danego agenta generuja lepszy lub przynajmniej taki samy koszt
"""
class ComputeBetterOrEqualBehaviour(CyclicBehaviour):
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

    def computeChangesLimit(self, sigma, cost):
        lenght = len(sigma)
        changes = round((cost - lenght * self.fAgent.pricePerEl)/self.fAgent.pricePerChange)
        return changes



    def createSetBetter(self, changesLimit):                                                                # to do 
        #we should create subset that we make less changes than changesLimit 
        toCreate = self.fAgent.itemsToCreate #the dictionary how many of which items should be created

    def createSetEqual(self, changes):                                                                      # to do 
        #we should create subset that we make exactly the same changes 
        toCreate = self.fAgent.itemsToCreate #the dictionary how many of which items should be created


    async def run(self):
        msg = await self.receive(timeout = 5)
        if msg is not None:
            #print("Got a message!")
            if(msg.body is not ""):
                sigma = self.parseMessage(msg.body)
                cost = self.fAgent.getMyCost(msg.body, sigma)
                changes = self.computeChangesLimit(sigma, cost)
                response = []
                response.append(self.createSetBetter(changes))
                response.append("break")
                response.append(self.createSetEqual)
                msgResp = Message(to=str(msg.sender))     # Instantiate the message
                msgResp.set_metadata("performative", "inform")
                msgResp.set_metadata("language","list" )
                msgResp.set_metadata("conversation-id", "1")
                msgResp.body = str(response)
                await self.send(msgResp)

    async def on_end(self):
        await self.agent.stop()