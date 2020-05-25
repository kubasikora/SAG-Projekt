from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy


class StateWaitForNextRound(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    async def run(self):
        self.fAgent.logger.log_info("Waiting for coworkers")
        # in this state we need to check if all coworkers are active and ready to start the next round
        #right now everyone has computet new sigma so all we have to di is to check what kind of message we got from our active mates

        #firstly we should inform then that we are ready

        for co in self.fAgent.activeCoworkers:
            msg = Message(to=co)
            msg.set_metadata("performative", "inform")
            msg.set_metadata("language","boolean" )
            msg.set_metadata("conversation-id", "1")
            msg.body = str(True)
            await self.send(msg)

        waitingCoworkers = deepcopy(self.fAgent.activeCoworkers)

        #firstly we should check saved messages
        msgToRemove = []
        for msg in self.fAgent.mailboxForLater:
            if msg.metadata["performative"] == "inform" and msg.metadata["language"] == "boolean" :
                msgToRemove.append(msg)
                waitingCoworkers.remove(str(msg.sender))
                if msg.body == "False":
                    self.fAgent.activeCoworkers.remove(str(msg.sender))
        for msg in msgToRemove:
            self.fAgent.mailboxForLater.remove(msg)
        while len(waitingCoworkers) > 0:
            resp = await self.receive(timeout=10)
            if resp is not None:
                sender = str(resp.sender)
                if resp.metadata["performative"] == "inform" and resp.metadata["language"] == "boolean" :
                    waitingCoworkers.remove(sender)
                    if resp.body == "False":
                        self.fAgent.activeCoworkers.remove(sender)
                else:
                    self.fAgent.saveMessage(msg)
        
        self.set_next_state(STATE_PROPOSE)

