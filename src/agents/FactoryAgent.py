import time
from spade.agent import Agent
from states import *
from spade.behaviour import FSMBehaviour
from spade.template import Template
from behaviours import ComputeAgentsCostBehaviour, ComputeRiskBehaviour, ComputeBetterOrEqualBehaviour
from Logger import Logger

class NegotiateFSMBehaviour(FSMBehaviour):
    def __init__(self, agent):
        FSMBehaviour.__init__(self)
        self.fAgent = agent

    async def on_end(self):
        self.fAgent.logger.log_success(f"Finishing at state {self.current_state}")
        #await self.agent.stop()

class FactoryAgent(Agent):
    def __init__(self, jid, password, name, pricePerEl, pricePerChange, sameIndexes , coworkers):
        super(FactoryAgent, self).__init__(jid, password)
        self.nameMy = name
        self.logger = Logger(name)
        self.Myjid = jid
        self.pricePerChange = pricePerChange
        self.pricePerEl = pricePerEl
        self.sameIndexes = sameIndexes
        self.myCalculatedCosts = dict()
        self.allCalculatedCosts = dict()
        self.coworkers = coworkers
        self.activeCoworkers = coworkers
        self.B0 = []
        self.currentSigma = []
        self.mailboxForLater = []
        self.worst = 0
        self.itemsToCreate = dict()
        self.B0prim = []

    def saveMatesBest(self, coworker, sigma):
        if sigma not in self.matesOptimal[coworker]:
            self.matesOptimal[coworker].append(sigma)

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
    def clearTables(self):
        self.myProposals = []
        self.myWorstProposal = []
        self.matesProposals = dict() # it will be something dictionary where string will be a key for list of lists 
        for col in self.coworkers:
            self.matesProposals[col] = []
        self.matesOptimal = dict() # it will be something dictionary where string will be a key for list of lists 
        for col in self.coworkers:
            self.matesOptimal[col] = []   
    
    def getCostAll(self, string):
        string = string.replace(" ", "")  
        if string in self.allCalculatedCosts:
            return self.allCalculatedCosts[string]
        else:
            return -1
    def setCostAll(self, string, cost):
        string = string.replace(" ", "")  
        self.allCalculatedCosts[string] = cost
    def saveMessage(self, msg):
        self.mailboxForLater.append(msg)
    
    async def setup(self):
        fsm = NegotiateFSMBehaviour(self)
        templateStates = Template()
        templateStates.to = self.Myjid
        templateStates.metadata = {"conversation-id": "1"}
        templateCost = Template()
        templateCost.to = self.Myjid
        templateCost.metadata = {"conversation-id": "2"}
        templateSets = Template()
        templateSets.to = self.Myjid
        templateSets.metadata = {"conversation-id": "3"}
        templateRisks = Template()
        templateRisks.to = self.Myjid
        templateRisks.metadata = {"conversation-id": "4"}

        fsm.add_state(name=STATE_INIT, state=StateInitial(self), initial=True)
        fsm.add_state(name=STATE_COMPUTE_B0, state=StateComputeB0(self))
        fsm.add_state(name=STATE_PROPOSE, state=StatePropose(self))
        fsm.add_state(name=STATE_WAIT_FOR_PROPSALS, state=StateWaitForProposals(self))
        fsm.add_state(name=STATE_COMPUTE_PROPOSALS, state=StateComputeProposals(self))
        fsm.add_state(name=STATE_COMPUTE_RISK, state=StateComputeRisk(self))
        fsm.add_state(name=STATE_COMPUTE_CONCESSION, state=StateComputeConcession(self))
        fsm.add_state(name=STATE_WAIT_FOR_NEXT_ROUND, state=StateWaitForNextRound(self))
        fsm.add_state(name=STATE_NOT_ACTIVE, state=StateNotActive(self))
        fsm.add_transition(source=STATE_INIT, dest=STATE_INIT)
        fsm.add_transition(source=STATE_INIT, dest=STATE_COMPUTE_B0)
        fsm.add_transition(source=STATE_COMPUTE_B0, dest=STATE_PROPOSE)
        fsm.add_transition(source=STATE_PROPOSE, dest=STATE_WAIT_FOR_PROPSALS)
        fsm.add_transition(source=STATE_WAIT_FOR_PROPSALS, dest=STATE_COMPUTE_PROPOSALS) # compute_proposals might be final if agreement found
        fsm.add_transition(source=STATE_COMPUTE_PROPOSALS, dest=STATE_COMPUTE_RISK)
        fsm.add_transition(source=STATE_COMPUTE_PROPOSALS, dest=STATE_NOT_ACTIVE)
        fsm.add_transition(source=STATE_COMPUTE_RISK, dest=STATE_COMPUTE_CONCESSION)
        fsm.add_transition(source=STATE_COMPUTE_RISK, dest=STATE_WAIT_FOR_NEXT_ROUND)
        fsm.add_transition(source=STATE_COMPUTE_CONCESSION, dest=STATE_WAIT_FOR_NEXT_ROUND)
        fsm.add_transition(source=STATE_COMPUTE_CONCESSION, dest=STATE_NOT_ACTIVE)
        fsm.add_transition(source=STATE_WAIT_FOR_NEXT_ROUND, dest=STATE_PROPOSE)

        cacb = ComputeAgentsCostBehaviour(self)
        csb = ComputeBetterOrEqualBehaviour(self)
        crb = ComputeRiskBehaviour(self)

        self.add_behaviour(fsm, templateStates)
        self.add_behaviour(cacb, templateCost)
        self.add_behaviour(crb, templateRisks)
        self.add_behaviour(csb, templateSets)