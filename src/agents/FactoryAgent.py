import datetime
from spade.agent import Agent
from spade.template import Template
from messages import *
from behaviours import *
from Logger import Logger
import asyncio

PERIOD = 10

class FactoryAgent(Agent):
    def __init__(self, jid, password, name, pricePerEl, pricePerChange, sameIndexes, coworkers, manager, active = True, notActiveCovorkers = []):
        super(FactoryAgent, self).__init__(jid, password)
        self.active = active
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
        for c in notActiveCovorkers:
            self.activeCoworkers.remove(c)
        self.B0 = []
        self.currentSigma = []
        self.mailboxForLater = []
        self.worst = 0
        self.itemsToCreate = dict()
        self.B0prim = []
        self.manager = manager
        self.optimal_result = None

        self.fsm = None
        self.crb = None
        self.csb = None
        self.cacb = None
        self.wb = None

        self.logger.log_warning("init done")

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

    async def stopAllBehaviours(self):
        for b in self.behaviours:
            b.kill()
        await self.stop()


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
    
    def killRandomBehaviour(self, i):
        if( i == 0):
            self.cacb.kill()
        elif(i == 1):
            self.crb.kill()
        elif(i == 2):
            self.csb.kill()

    
    async def setup(self):
        self.logger.log_success("Setting up agent behaviours")
                
        if self.fsm is None and self.active == True:
            self.fsm = NegotiateFSMBehaviour(self)
            templateStates = StatesMessage.template(self.Myjid)
            self.add_behaviour(self.fsm, templateStates)
        
        if self.cacb is None:
            self.cacb = ComputeAgentsCostBehaviour(self)
            templateCost = CostMessage.template(self.Myjid)
            self.add_behaviour(self.cacb, templateCost)

        if self.crb is None:
            self.crb = ComputeRiskBehaviour(self)
            templateRisks = RiskMessage.template(self.Myjid)
            self.add_behaviour(self.crb, templateRisks)           

        if self.csb is None:
            self.csb = ComputeBetterOrEqualBehaviour(self)    
            templateSets = SetsMessage.template(self.Myjid)
            self.add_behaviour(self.csb, templateSets)

        if self.wb is None:
            self.wb = WatchdogBehaviour(self, PERIOD, datetime.datetime.now() + datetime.timedelta(seconds=1))
            templateWatchdog = WatchdogMessage.template(self.Myjid)
            self.add_behaviour(self.wb, templateWatchdog)
        
        self.logger.log_success("All behaviours set up")
        

        