from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy

def parseSets(string): # the format of the string [[[],[], ..], 'break', [[],[],...]]
    string = string.replace(" ", "")
    lists = string.split("break")
    toReturn = []
    for l in lists:
        l = l.replace("'", "")
        sigmas = l.split("]")
        converted = []
        for sigma in sigmas:
            sigma = sigma.replace("[", "")            
            if( len(sigma)> 0 and sigma[0] == ","):
                sigma = sigma[1:]
            if(len(sigma)) > 0:
                nums = sigma.split(",")
                convertedSigma = []
                for n in nums:
                    convertedSigma.append(int(n))
                converted.append(convertedSigma)
        toReturn.append(converted)

    return toReturn


def removeDuplicats(elements):
    toReturn = []
    for el in elements:
        if el not in toReturn:
            toReturn.append(el)
    return toReturn
        

class StateComputeConcession(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        print("Compute concession, my name "+ self.fAgent.nameMy)
        #1. we should propose something what is at least as good for our mates as the one whe proposed before
        #2. we should propopse something that for one agent is better
        for co in self.fAgent.activeCoworkers:
            msg = Message(to=co)     # Instantiate the message
            msg.set_metadata("performative", "request")
            msg.set_metadata("language","list" )
            msg.set_metadata("conversation-id", "3")
            msg.body = str(self.fAgent.currentSigma)
            await self.send(msg)

        waitingCoworkers = deepcopy(self.fAgent.activeCoworkers)
        matesPropositions = []
        while len(waitingCoworkers) > 0:
            msg = await self.receive(timeout = 5)
            if msg is not None:
                if msg.metadata["performative"] == "inform" and msg.metadata["language"] == "list" :
                    sender = str(msg.sender)
                    matesPropositions.append(parseSets(msg.body))
                    waitingCoworkers.remove(sender)
                else:
                    self.fAgent.saveMessage(msg)
        print("we have propositions!")
        #right not in matesPropositions we have got elements for each of active coworkers
        #we should combine it so that we should check that an element which we got from one coworker is also in others and that
        #en element is better at least for one agent
        sigmas = []
        numOfCoworkers = len(matesPropositions)
        for i in range(len(matesPropositions)):
            for sigma in matesPropositions[i][0]: #sigmas which are better 
                toAdd = True
                for j in range(len(matesPropositions)):
                    if sigma not in matesPropositions[j][0] and sigma not in matesPropositions[j][1]:
                        toAdd = False
                        break
                if toAdd == True:
                    sigmas.append(sigma)
                    
        sigmas = removeDuplicats(sigmas)
        





        #3. we should change the risk 


        #4. we should propose something that has lower cost than what we proposed before

        #5. from this set we should chose something what has the smallest cost 