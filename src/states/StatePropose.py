from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from spade.message import Message
from .metadata import *


class StatePropose(State):
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent


    #need to wait for other agen to skip this state
    async def run(self):
        print("Starting negotiation, my name "+ self.agent.getName())
        sigma = self.fAgent.getCurrentSigma()
        myProposition = self.fAgent.getMyProposals()
        if sigma not in myProposition:
            myProposition.append(sigma)
        activeCoworkers = self.fAgent.getActiveCoworkers()
        for coworker in activeCoworkers:
            msg = Message(to=coworker)
            msg.set_metadata("performative", "propose")
            msg.set_metadata("language","list" )
            #msg.set_metadata("conversation-id", "1") #here an error occured -> the agent got message too early
            #msg.body = str(sigma)
            await self.send(msg)
        #self.set_next_state(STATE_COMPUTE_PROPOSALS)
        #bezposrednia zmiana stanu do oczekiwania na przyjecie odpowiedzi

        
