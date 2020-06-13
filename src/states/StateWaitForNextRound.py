from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy
from messages import StatesMessage, WatchdogMessage


MAX_TIMES = 100

class StateWaitForNextRound(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent


    def clearMailBox(self):
        toRemove = []
        for msg in self.fAgent.mailboxForLater:
            if msg.metadata["performative"] == "inform" and msg.metadata["language"] == "boolean":
                toRemove.append(msg)
        for msg in toRemove:
            self.fAgent.mailboxForLater.remove(msg)

    async def run(self):
        self.fAgent.logger.log_info("Waiting for coworkers")
        # in this state we need to check if all coworkers are active and ready to start the next round
        #right now everyone has computet new sigma so all we have to di is to check what kind of message we got from our active mates

        #firstly we should inform then that we are ready

        for co in self.fAgent.activeCoworkers:
            msg = StatesMessage(to=co, body=True)
            msg.set_metadata("language", "boolean")
            await self.send(msg)

        waitingCoworkers = deepcopy(self.fAgent.activeCoworkers)

        #firstly we should check saved messages
        msgToRemove = []
        for msg in self.fAgent.mailboxForLater:
            if msg.metadata["performative"] == "inform" and msg.metadata["language"] == "boolean" and str(msg.sender) in waitingCoworkers:
                msgToRemove.append(msg)
                waitingCoworkers.remove(str(msg.sender))
                if msg.body == "False":
                    self.fAgent.activeCoworkers.remove(str(msg.sender))
        for msg in msgToRemove:
            self.fAgent.mailboxForLater.remove(msg)
        count = 0
        while len(waitingCoworkers) > 0:
            resp = await self.receive(timeout=10)
            if resp is not None:
                sender = str(resp.sender)
                if resp.metadata["performative"] == "inform" and resp.metadata["language"] == "boolean" and str(resp.sender) in waitingCoworkers:
                    waitingCoworkers.remove(sender)
                    if resp.body == "False":
                        self.fAgent.activeCoworkers.remove(sender)
                else:
                    self.fAgent.saveMessage(msg)
            else:
                count = count + 1 
                if count < MAX_TIMES:
                    for cw in self.fAgent.activeCoworkers():
                        msg = StatesMessage(to=cw, body=True)
                        msg.set_metadata("language", "boolean")
                        await self.send(msg)
                else:
                    for c in waitingCoworkers:
                        alarmMsg = WatchdogMessage(to = self.fAgent.manager, body = str(WorkingState.COMPLAINT)+""+c)
                        await self.send(alarmMsg)
                    break
        self.clearMailBox()
        self.set_next_state(STATE_PROPOSE)

