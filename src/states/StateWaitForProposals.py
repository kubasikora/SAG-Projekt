from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy
from behaviours import WorkingState

MAX_TIME = 5 # 5 min is the max time of waiting for all other guys

def parseMessage(body):
    without = body.replace("[", "")
    without = without.replace("]", "")
    without = without.replace(" ", "")
    nums = without.split(",")
    toReturn = []
    for num in nums:
        toReturn.append(int(num))
    return toReturn  

class StateWaitForProposals(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        waitingActiveCoworkers = deepcopy(self.fAgent.activeCoworkers)
        self.fAgent.logger.log_info(f"Waiting for proposals from {waitingActiveCoworkers}")
        toRemove = []
        proposals = dict()
        for msg in self.fAgent.mailboxForLater:
            if msg.metadata["performative"] == "propose" and msg.metadata["language"] == "list" :
                #print(msg.sender)
                toRemove.append(msg)
                sender = str(msg.sender)
                waitingActiveCoworkers.remove(sender)
                proposals[sender] = parseMessage(msg.body)
        for msg in toRemove:
            self.fAgent.mailboxForLater.remove(msg)
        counter = 0
        while(len(waitingActiveCoworkers)>0):
            msg = await self.receive(timeout = 60)
            if msg is not None:
                if msg.metadata["performative"] == "propose" and msg.metadata["language"] == "list" and str(msg.sender) in waitingActiveCoworkers :
                    sender = str(msg.sender)
                    waitingActiveCoworkers.remove(sender)
                    proposals[sender] = parseMessage(msg.body)                    
                else:
                    self.fAgent.saveMessage(msg)
            else: 
                counter = counter + 1
                if (counter < MAX_TIME):
                    sigma = self.fAgent.myProposals[len(self.fAgent.myProposals) - 1]
                    for c in waitingActiveCoworkers:
                        retry = StatesMessage(to=c, body=sigma)
                        retry.set_metadata("performative", "propose")
                        retry.set_metadata("language","list")
                        await self.send(retry)
                else:
                    for c in waitingActiveCoworkers:
                        alarmMsg = WatchdogMessage(to = self.fAgent.manager, body = str(WorkingState.COMPLAINT)+""+c)
                        await self.send(alarmMsg)
        #print("I got all proposals "+self.fAgent.nameMy)
        for (mate, seq) in proposals.items():
            if seq not in self.fAgent.matesProposals[mate]:
                self.fAgent.matesProposals[mate].append(seq)
        #print("End "+self.fAgent.nameMy)
        self.set_next_state(STATE_COMPUTE_PROPOSALS)

