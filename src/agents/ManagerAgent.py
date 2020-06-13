import time
from spade.agent import Agent
from .FactoryAgent import FactoryAgent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template
from Logger import Logger
from behaviours import ControlSubordinatesBehaviour
from messages import *
import json
import asyncio
import datetime

PERIOD = 20

class DeputeBehaviour(OneShotBehaviour): 
    def __init__(self, agent, params): #params is a dic of (jid, password, name, priceEle, priceChan, sameIndex, coworkers)
        OneShotBehaviour.__init__(self)
        self.agent = agent
        self.params = params
        #self.agent.logger.log_info(f"DeputeBehaviour for {self.jidToSend} created")

    async def run(self):
        dictTest = self.agent.task
        for p in self.params:
            jid =p["jid"]
            self.agent.logger.log_info(f"Adding {jid} to the team")
            created = FactoryAgent(p["jid"], p["password"],p["name"],p["priceEle"], p["priceChan"], p["sameIndex"],p["coworkers"], "manager@localhost")
            self.agent.workers.append(created)
            await created.start()
            created.web.start(hostname="localhost", port="10000")
            self.agent.logger.log_info(f"DeputeBehaviour for {jid} created")

        for p in self.params:
            jid = p["jid"]
            msg = StatesMessage(to=jid, body=dictTest)
            msg.set_metadata("performative", "request")     # Instantiate the message
            await self.send(msg)
            self.agent.logger.log_info(f"Task sent to {jid}")

        self.agent.logger.log_info(f"Every task sent")

    async def on_end(self): 
        self.kill()

class MonitorAgentActivityBehaviour(CyclicBehaviour):
    def __init__(self, agent, workers):
        CyclicBehaviour.__init__(self)
        self.agent = agent
        self.workers = dict((worker, False) for worker in workers)
        self.agent.logger.log_info("MonitorAgentActivityBehaviour created")

    async def on_start(self):
        for _, worker in enumerate(self.workers):
            message = WatchdogMessage(to=worker, body="{message: 'Hello'}")
            await self.send(message)
    def isAgentActive(self, jid):
        return not self.workers[jid]
    
    def getNotActiveDespite(self, jid):
        toRet = []
        for key, value in self.workers.items():
            if(key != jid and value == True):
                toRet.append(key)
        return toRet


    async def run(self):
        message = await self.receive(timeout=1)
        if message is not None:
            self.agent.logger.log_info(f"Agent {message.sender} reported inactivity")
            self.workers[str(message.sender)] = True
            
            # do wydzielenia do osobnej funkcji
            self.agent.logger.log_info(f"Agent {self.workers} ")
            logic_accumulator = True
            for key in self.workers:
                logic_accumulator &= self.workers[key]

            if logic_accumulator:
                # all agents reported inactivity
                self.agent.logger.log_info(f"All agents are inactive")
                fwd = ResultsMessage(to=message.to, body=message.body)
                await self.send(fwd) # forward message to receiver behaviour
            
    async def on_end(self):
        await self.agent.stop()

class ReceiveResultBehaviour(CyclicBehaviour):
    def __init__(self, agent):
        CyclicBehaviour.__init__(self)
        self.agent = agent
        self.agent.logger.log_info("ReceiveResultBehaviour created")

    async def run(self):
        message = await self.receive(timeout=1)
        if message is not None:
            result = json.loads(message.body)
            self.agent.logger.log_success(f"Got optimal sequence {result['sequence']} with total cost of {result['cost']}")
            self.kill()

    async def on_end(self):
        await self.agent.stop()

class ManagerAgent(Agent):
    def __init__(self, jid, password, workersParams, task): #workersParams to lista slownikow (jid, password, name, priceEle, priceChan, sameIndex, coworkers)
        Agent.__init__(self, jid, password)
        self.MyJid = jid
        self.logger = Logger(self.jid)
        self.workersParams = workersParams
        self.task = task
        self.workers = []

    def findWorker(self, jid):
        i = 0
        for worker in self.workers:
            if worker.Myjid == jid:
                return worker, i
            i = i + 1
    
    def isAgentActive(self, jid):
        return self.agentMonitor.isAgentActive(jid)

    def getNotActiveDespite(self, jid):
        return self.agentMonitor.getNotActiveDespite(jid)
    async def setup(self):

        self.creator = DeputeBehaviour(self, self.workersParams)
        self.add_behaviour(self.creator)
        
        workersJid = []
        for workerParams in self.workersParams:
            workersJid.append(workerParams["jid"])  # to give params to rest behaviours

        receiver_template = ResultsMessage.template(self.MyJid)
        self.waitForOptimalSequence = ReceiveResultBehaviour(self)
        self.add_behaviour(self.waitForOptimalSequence, receiver_template) 
        
        watchdog_template = WatchdogMessage.template(self.MyJid)
        self.agentControler = ControlSubordinatesBehaviour(self, PERIOD, datetime.datetime.now() + datetime.timedelta(seconds=5), workersJid)
        self.add_behaviour(self.agentControler, watchdog_template)

        monitor_template = InactiveMessage.template(self.MyJid)
        self.agentMonitor = MonitorAgentActivityBehaviour(self, workersJid)
        self.add_behaviour(self.agentMonitor, monitor_template)


        self.logger.log_info("Manager has started")