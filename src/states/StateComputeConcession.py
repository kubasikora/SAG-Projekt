from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy
import random
from messages import *
from behaviours import WorkingState

MAX_TIMES = 4

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

    def linkMessages(self, allMessages, allMessagesLen):
        keys = allMessages.keys()
        toRet = [] # list of strings 
        for k in keys:
            length = len(allMessages[k])
            if (length != allMessagesLen[k]):
                self.fAgent.logger.log_error("There is a problem with messages!!")
            oneAgents = [None] * length
            for m in allMessages[k]:
                which = int(m.metadata["which"]) - 1
                oneAgents[which] = m.body
            msgAllBody = ""
            for string in oneAgents:
                msgAllBody = msgAllBody + string
            toRet.append(msgAllBody)
            # ... we should add messages in 
        return toRet

    async def run(self):
        self.fAgent.logger.log_info("Computing concession")
        #1. we should propose something what is at least as good for our mates as the one whe proposed before
        # we should propopse something that for one agent is better
        for co in self.fAgent.activeCoworkers:
            msg = SetsMessage(to=co, body=self.fAgent.currentSigma)     # Instantiate the message
            msg.set_metadata("performative", "request")
            msg.set_metadata("language","list")
            msg.body = str(self.fAgent.currentSigma)
            await self.send(msg)

        waitingCoworkers = deepcopy(self.fAgent.activeCoworkers)
        matesPropositionsAll = dict((worker, []) for worker in self.fAgent.activeCoworkers)
        matesPropositionsAllCount = dict((worker, -1) for worker in self.fAgent.activeCoworkers)
        matesPropositions = []
        counter = 0
        while len(waitingCoworkers) > 0:
            msg = await self.receive(timeout = 5)
            if msg is not None:
                if msg.metadata["performative"] == "inform" and msg.metadata["language"] == "list" and str(msg.sender) in waitingCoworkers :
                    sender = str(msg.sender)
                    if matesPropositionsAllCount[sender] == -1:
                        #first msg
                        matesPropositionsAllCount[sender] = int(msg.metadata["howMany"])
                    matesPropositionsAll[sender].append(msg)
                    if len(matesPropositionsAll[sender]) == matesPropositionsAllCount[sender]:
                        waitingCoworkers.remove(sender)
                else:
                    self.fAgent.saveMessage(msg)
            else:
                counter = counter + 1 
                self.fAgent.logger.log_info("we have not received and msgs from 5s")
                if counter > MAX_TIMES:
                    self.fAgent.logger.log_info(f"something is wrong with {len(waitingCoworkers)}")
                    for c in waitingCoworkers:
                        alarmMsg = WatchdogMessage(to = self.fAgent.manager, body = str(WorkingState.COMPLAINT)+" "+c)
                        await self.send(alarmMsg)
                        self.set_next_state(STATE_PROPOSE)
                        return
        
        #we received All msgs!
        allMsg = self.linkMessages(matesPropositionsAll, matesPropositionsAllCount)
        for s in allMsg:
            matesPropositions.append(parseSets(s))

        #right not in matesPropositions we have got elements for each of active coworkers
        #we should combine it so that we should check that an element which we got from one coworker is also in others and that
        #en element is better at least for one agent
        sigmas = []
        numOfCoworkers = len(matesPropositions)
        for i in range(len(matesPropositions)):
            for sigma in matesPropositions[i][0]: #sigmas which are better 
                toAdd = True
                for j in range(len(matesPropositions)):
                    if  i == j or (i != j and sigma not in matesPropositions[j][0] and sigma not in matesPropositions[j][1]):
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
                body = []
                body.append(s)
                body.append('break')
                body.append(self.fAgent.matesProposals[co][len(self.fAgent.matesProposals[co]) - 1])

                msg = RiskMessage(to=co, body=body)
                msg.set_metadata("performative", "request")
                msg.set_metadata("language", "list")
                await self.send(msg)

                received = False
                newRisk = 0.0
                counter = 0
                while received == False:
                    resp = await self.receive(timeout = 10)
                    if resp is not None: 
                        if resp.metadata["performative"] == "inform" and resp.metadata["language"] == "float" :
                            received = True
                            newRisk = float(resp.body)
                        else:
                            self.fAgent.saveMessage(resp)
                    else:
                        counter = counter + 1
                        if counter < MAX_TIMES:
                            await self.send(msg)
                        else:
                            self.fAgent.logger.log_error(f"something is wrong with {co}")
                            alarmMsg = WatchdogMessage(to = self.fAgent.manager, body = str(WorkingState.COMPLAINT)+" "+co)
                            await self.send(alarmMsg)
                            self.set_next_sate(STATE_PROPOSE)
                            return
                if newRisk <  myRisk:
                    # we found something what might be concession!
                    found = True
                    break

            if found == True:
                sigmasWithGoodRisk.append(s)


        #4. we should propose something that has lower cost than what we proposed before
        #5. from this set we should chose something what has the smallest cost 
        myOldCost = self.fAgent.getCostAll(str(self.fAgent.currentSigma))
        if myOldCost == -1:
            self.fAgent.logger.log_error("Error, my old cost is equal to -1") #this situation should not occure
        lowestCostFound = myOldCost # jesli znajdziemy cos co jest nizsze to to wybieramy
        bestSigmas = []
        for s in sigmasWithGoodRisk:
            tempCost = self.fAgent.getMyCost(str(s), s)
            costAllTemp = self.fAgent.getCostAll(str(s))
            if costAllTemp != -1 :
                tempCost = costAllTemp
            else:
                for co in self.fAgent.coworkers:
                    msg=CostMessage(to=co, body=s)
                    msg.set_metadata("save", "False")
                    await self.send(msg)

                    gotResponse = False
                    counter = 0
                    while gotResponse == False:
                        resp = await self.receive(timeout=5)
                        if resp is None:
                            counter = counter + 1
                            if counter < MAX_TIMES:
                                await self.send(msg)
                            else:
                                self.fAgent.logger.log_error("Error") #probably we should raise exception or something !!!!!!!!!!!!!
                                alarmMsg = WatchdogMessage(to = self.fAgent.manager, body = str(WorkingState.COMPLAINT)+" "+co)
                                await self.send(alarmMsg)
                                self.set_next_state(STATE_PROPOSE)
                                return
                        else:
                            if resp.metadata["performative"] == "inform" and resp.metadata["language"] == "int" and str(resp.sender) == co:
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
            self.fAgent.logger.log_success("We have true concession!!")
            chosen = random.choice(bestSigmas)
            if chosen in self.fAgent.B0:
                self.fAgent.B0.remove(chosen)
            if self.fAgent.getMyCost(str(self.fAgent.myWorstProposal), self.fAgent.myWorstProposal) < self.fAgent.getMyCost(str(chosen), chosen):
                self.fAgent.myWorstProposal = chosen

            self.fAgent.currentSigma = chosen
            self.set_next_state(STATE_WAIT_FOR_NEXT_ROUND)

        elif len(self.fAgent.B0 ) > 0:
            self.fAgent.logger.log_warning("No concession found, need to check B0 set")
            chosen = random.choice(self.fAgent.B0)
            self.fAgent.B0.remove(chosen)
            if self.fAgent.getMyCost(str(self.fAgent.myWorstProposal), self.fAgent.myWorstProposal) < self.fAgent.getMyCost(str(chosen), chosen):
                self.fAgent.myWorstProposal = chosen           
            self.fAgent.currentSigma = chosen
            self.set_next_state(STATE_WAIT_FOR_NEXT_ROUND)
        else: 
            self.set_next_state(STATE_NOT_ACTIVE)
            # new state to add!! 
        

