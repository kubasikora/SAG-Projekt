from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy
import random

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

    def computeRisk(self, my, others):
        myUtility = float(self.fAgent.worst - self.fAgent.getMyCost(str(my),my))
        if myUtility == 0.0:
            return 1.0
        #zwracamy najwieksze ryzyko
        risk = 0.0
        for o in others:
            utility = float(self.fAgent.worst - self.fAgent.getMyCost(str(o),o))
            temp = (myUtility - utility)/myUtility
            if(temp > risk):
                risk = temp
        return risk

    async def run(self):
        print("Compute concession, my name "+ self.fAgent.nameMy)
        #1. we should propose something what is at least as good for our mates as the one whe proposed before
        # we should propopse something that for one agent is better
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

        #2. We should not propose anything that we proposed previously
        for prev in self.fAgent.myProposals:
            if prev in sigmas:
                sigmas.remove(prev)

        
        #3. we should change the risk 
        others = []
        sigmasWithGoodRisk = []
        for co in self.fAgent.activeCoworkers:
            others.append(self.fAgent.matesProposals[co][len(self.fAgent.matesProposals[co]) - 1])

        for s in sigmas:
            myRisk = self.computeRisk(s,others)
            found = False
            for co in self.fAgent.activeCoworkers:
                msg = Message(to=co)
                msg.set_metadata("performative", "request")
                msg.set_metadata("language","list" )
                msg.set_metadata("conversation-id", "4")
                body = []
                body.append(s)
                body.append('break')
                body.append(self.fAgent.matesProposals[co][len(self.fAgent.matesProposals[co]) - 1])
                msg.body = str(body)
                await self.send(msg)

                received = False
                newRisk = 0.0
                while received == False:
                    resp = await self.receive(timeout = 5)
                    if resp is not None: 
                        if resp.metadata["performative"] == "inform" and resp.metadata["language"] == "float" :
                            received = True
                            newRisk = float(resp.body)
                        else:
                            self.fAgent.saveMessage(resp)
                if newRisk > myRisk:
                    # we found something what might be concession!
                    found = True
                    break

            if found == True:
                sigmasWithGoodRisk.append(s)


        #4. we should propose something that has lower cost than what we proposed before
        #5. from this set we should chose something what has the smallest cost 
        myOldCost = self.fAgent.getCostAll(str(self.fAgent.currentSigma))
        if myOldCost == -1:
            print("error ") #this situation should not occure
        lowestCostFound = myOldCost # jesli znajdziemy cos co jest nizsze to to wybieramy
        bestSigmas = []
        for s in sigmasWithGoodRisk:
            tempCost = self.fAgent.getMyCost(str(s), s)
            costAllTemp = self.fAgent.getCostAll(str(s))
            if costAllTemp != -1 :
                tempCost = costAllTemp
            else:
                for co in self.fAgent.coworkers:
                    msg=Message(to=cp)
                    msg.set_metadata("conversation-id", "2")
                    msg.set_metadata("performative", "request")
                    msg.body = str(s)
                    await self.send(msg)
                    gotResponse = False
                    while gotResponse == False:
                        resp = await self.receive(timeout=5)
                        if resp is None:
                            print("Error") #probably we should raise exception or something !!!!!!!!!!!!!
                        else:
                            if resp.metadata["performative"] == "inform" and resp.metadata["language"] == "int" :
                                tempCost = tempCost + int(resp.body)
                                gotResponse = True
                            else:
                                self.fAgent.saveMessage(resp)
                self.fAgent.setCostAll(str(s), tempCost)
            if tempCost == lowestCostFound and tempCost < myOldCost:
                bestSigmas.append(s)
            elif tempCost < lowestCostFound:
                bestSigmas.clear()
                bestSigmas.append(s)
                lowestCostFound = tempCost
        
        #Finally we have got set of true concession !!! we should chose one of them 
        if len(bestSigmas) > 0:
            print("we have true concession!!")
            chosen = random.choice(bestSigmas)
            if chosen in self.fAgent.B0:
                self.fAgent.B0.remove(chosen)
            if self.fAgent.getMyCost(str(self.fAgent.myWorstProposal), self.fAgent.myWorstProposal) < self.fAgent.getMyCost(str(chosen), chosen):
                self.fAgent.myWorstProposal = chosen

            self.fAgent.currentSigma = chosen
            self.set_next_state(STATE_WAIT_FOR_NEXT_ROUND)

        elif len(self.fAgent.B0 > 0):
            print("nope, need to check B0 set")
            chosen = random.choice(self.fAgent.B0)
            self.fAgent.B0.remove(chosen)
            if self.fAgent.getMyCost(str(self.fAgent.myWorstProposal), self.fAgent.myWorstProposal) < self.fAgent.getMyCost(str(chosen), chosen):
                self.fAgent.myWorstProposal = chosen           
            self.fAgent.currentSigma = chosen
            self.set_next_state(STATE_WAIT_FOR_NEXT_ROUND)
        else: 
            print("should change state to recomputing bpi if it is possible")
            # new state to add!! 
        
