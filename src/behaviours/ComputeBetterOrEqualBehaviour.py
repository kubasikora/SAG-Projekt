from spade.behaviour import CyclicBehaviour
from agents import FactoryAgent
from spade.message import Message
from messages import StatesMessage

MAX_LENGTH = 1000 * 40
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




    def createSets(self, cost):
        better = []
        equal = []
        for sigma in self.fAgent.B0prim:
            if (self.fAgent.getMyCost(str(sigma), sigma) < cost):
                better.append(sigma)
            elif (self.fAgent.getMyCost(str(sigma), sigma) == cost):
                equal.append(sigma)         
        for co in self.fAgent.coworkers:
            for sigma in self.fAgent.matesOptimal[co]:
                if (self.fAgent.getMyCost(str(sigma), sigma) < cost):
                    better.append(sigma)
                elif (self.fAgent.getMyCost(str(sigma), sigma)== cost):
                    equal.append(sigma)   
        return [better, equal]  

    def divideString(self, response):
        toRet = []
        howMany = int(float(len(response)) / float(MAX_LENGTH)) + 1
        for i in range(howMany):
            substr = ""
            if i == howMany - 1 :
                substr = response[i*MAX_LENGTH:] 
            else:
                substr = response[i*MAX_LENGTH: (i+1)*MAX_LENGTH ]   
            toRet.append(substr)    
        return howMany, toRet                  


    async def run(self):
        msg = await self.receive(timeout = 5)
        if msg is not None:
            #print("Got a message!")
            if(msg.body is not ""):
                sigma = self.parseMessage(msg.body)
                cost = self.fAgent.getMyCost(msg.body, sigma)
                response = []
                sets = self.createSets(cost)
                response.append(sets[0])
                response.append("break")
                response.append(sets[1])

                howMany, subsets = self.divideString(str(response))

                for i in range(howMany):
                    msgResp = StatesMessage(to=msg.sender, body=subsets[i])
                    msgResp.set_metadata("language", "list")
                    msgResp.set_metadata("which" , str(i+1)) # bedziemy wysylac pojedynczo
                    msgResp.set_metadata("howMany", str(howMany))
                    await self.send(msgResp)
