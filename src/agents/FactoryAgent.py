import time
from spade.agent import Agent
from states import *
from spade.behaviour import FSMBehaviour
from spade.template import Template
from behaviours import ComputePriceBehaviour

class NegotiateFSMBehaviour(FSMBehaviour):
    async def on_end(self):
        print("Finishing at state "+ self.current_state)
        await self.agent.stop()



class FactoryAgent(Agent):
    def __init__(self, jid, password, name, pricePerEl, pricePerChange, sameIndexes , coworkers):
        super(FactoryAgent, self).__init__(jid, password)
        self.nameMy = name
        self.Myjid = jid
        self.pricePerChange = pricePerChange
        self.pricePerEl = pricePerEl
        self.sameIndexes = sameIndexes
        self.myCalculatedCosts = dict()
        self.allCalculatedCosts = dict()
        self.coworkers = coworkers

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

    def getType(self, index):
        if index in self.sameIndexes[0] : 
            return "a"
        elif index in self.sameIndexes[1]:
            return "b"
        else:
            return "c"

    def computeCost(self, sequence):
        cost = len(sequence) * self.pricePerEl
        lastType = "n"
        for s in sequence:
            c = self.getType(s)
            if c != lastType:
                cost = cost + self.pricePerChange
                lastType = c
        cost = cost - self.pricePerChange
        return cost

    def getMyCost(self, string, sequence):
        string = string.replace(" ", "")     
        if string in self.myCalculatedCosts:
            return self.myCalculatedCosts[string]
        else:
            cost = self.computeCost(sequence)
            self.myCalculatedCosts[string] = cost
            return cost

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
    def getCoworkers(self):
        return self.coworkers
    async def setup(self):
        fsm = NegotiateFSMBehaviour()
        templateStates = Template()
        #templateStates.sender = "manager@localhost"
        templateStates.to = self.Myjid
        #templateStates.metadata = {"performative": "request", "language":"dictionary"}
        templateStates.metadata = {"conversation-id": "1"}
        templateCost = Template()
        templateCost.to = self.Myjid
        templateCost.metadata = {"conversation-id": "2"}

        fsm.add_state(name=STATE_INIT, state=StateInitial(self), initial=True)
        fsm.add_state(name=STATE_COMPUTE_B0, state=StateComputeB0(self))
        fsm.add_transition(source=STATE_INIT, dest=STATE_INIT)
        fsm.add_transition(source=STATE_INIT, dest=STATE_COMPUTE_B0)
        #fsm.add_transition(source=STATE_COMPUTE_B0, dest=STATE_PROPOSE)

        cpb = ComputePriceBehaviour(self)

        self.add_behaviour(fsm, templateStates)
        self.add_behaviour(cpb, templateCost)