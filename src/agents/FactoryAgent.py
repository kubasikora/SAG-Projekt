import time
from spade.agent import Agent
from states import *
from spade.behaviour import FSMBehaviour
from spade.template import Template

class NegotiateFSMBehaviour(FSMBehaviour):
    async def on_end(self):
        print("Finishing at state "+ self.current_state)
        await self.agent.stop()



class FactoryAgent(Agent):
    def __init__(self, jid, password, name, pricePerEl, pricePerChange, sameIndexes ):
        super(FactoryAgent, self).__init__(jid, password)
        self.nameMy = name
        self.Myjid = jid
        self.pricePerChange = pricePerChange
        self.pricePerEl = pricePerEl
        self.sameIndexes = sameIndexes

    def getName(self):
        return self.nameMy
    def getPricePerPiece(self):
        return self.pricePerEl
    def getPricePerChange(self):
        return self.pricePerChange
    def getSameIndexes(self):
        return self.sameIndexes
    def setToProduce(self, itemsToCreate):
        self.itemsToCreate = itemsToCreate
    def setWorst(self, worst):
        self.worst = worst
    def setB0prim(self, B0prim):
        self.B0prim = B0prim
    def getB0prim(self):
        return self.B0prim
    def getWorst(self):
        return self.worst
    def clearTable(self):
        self.myProposals = []
        self.mateAProposals = []
        self.mateBProposals = []

    async def setup(self):
        fsm = NegotiateFSMBehaviour()
        template = Template()
        template.sender = "manager@localhost"
        template.to = self.Myjid
        template.metadata = {"performative": "request", "language":"dictionary"}
        fsm.add_state(name=STATE_INIT, state=StateInitial(self), initial=True)
        self.add_behaviour(fsm, template)