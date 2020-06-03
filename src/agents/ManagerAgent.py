import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template
from Logger import Logger
from behaviours import ControlSubordinatesBehaviour
from messages import WatchdogMessage, WatchdogTemplate
import json
import asyncio
import datetime

PERIOD = 20

class DeputeBehaviour(OneShotBehaviour):
    def __init__(self, agent, jidToSend):
        OneShotBehaviour.__init__(self)
        self.agent = agent
        self.jidToSend = jidToSend
        self.agent.logger.log_info(f"DeputeBehaviour for {jidToSend} created")

    async def run(self):
        self.agent.logger.log_info(f"Adding {self.jidToSend} to the team")
        msg = Message(to=self.jidToSend)     # Instantiate the message
        msg.set_metadata("conversation-id", "1")
        msg.set_metadata("performative", "request")  # Set the "inform" FIPA performative
        msg.set_metadata("language","dictionary" )
        # dictTest={0:0, 1:0, 2:0, 3:4, 4:0, 5:7, 6:7, 7:8, 8:0, 9:0 , 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:9, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0, 25:6, 26:0}
        dictTest={0:0, 1:0, 2:0, 3:4, 4:0, 5:7, 6:7, 7:8, 8:0, 9:0 , 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:9, 17:5, 18:0, 19:0, 20:1, 21:9, 22:3, 23:0, 24:0, 25:6, 26:0}
        msg.body = str(dictTest)
        await self.send(msg)
        self.agent.logger.log_info(f"Task sent to {self.jidToSend}")

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
            message = WatchdogMessage(worker, body="{message: 'Hello'}")
            await self.send(message)

    async def run(self):
        message = await self.receive(timeout=1)
        if message is not None:
            self.agent.logger.log_info(f"Agent {message.sender} reported inactivity")
            self.workers[message.sender] = True
            
            # do wydzielenia do osobnej funkcji
            logic_accumulator = True
            for key in self.workers:
                logic_accumulator &= self.workers[key]

            if logic_accumulator:
                # all agents reported inactivity
                fwd = Message(to=message.to)
                fwd.set_metadata("performative", "inform")
                fwd.set_metadata("conversation-id", "results")
                fwd.body = message.body
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
    def __init__(self, jid, password, workers):
        Agent.__init__(self, jid, password)
        self.logger = Logger(self.jid)
        self.workers = workers

    def findWorker(self, jid):
        for worker in self.workers:
            if worker.Myjid == jid:
                return worker

    async def setup(self):
        receiver_template = Template()
        receiver_template.set_metadata("performative", "inform")
        receiver_template.set_metadata("conversation-id", "results")
        self.waitForOptimalSequence = ReceiveResultBehaviour(self)
        self.add_behaviour(self.waitForOptimalSequence, receiver_template)

        self.painterA = DeputeBehaviour(self, "paintera@localhost")
        self.add_behaviour(self.painterA)

        self.welderA = DeputeBehaviour(self, "weldera@localhost")
        self.add_behaviour(self.welderA)

        self.assemblyA = DeputeBehaviour(self, "assemblya@localhost")
        self.add_behaviour(self.assemblyA)
   
        monitor_template = WatchdogTemplate()
        self.subordinates = ["paintera@localhost", "weldera@localhost", "assemblya@localhost"]
        self.agentMonitor = ControlSubordinatesBehaviour(self, PERIOD, datetime.datetime.now() + datetime.timedelta(seconds=1), self.subordinates)

        self.add_behaviour(self.agentMonitor, monitor_template)
        

        #checking how restart works :) 

        for worker in self.workers:
            await worker.stop()
            self.logger.log_error(f"Manager has stopped {worker.Myjid}")
            await worker.start(True)
            self.logger.log_error(f"Manager has started {worker.Myjid}")
            #future = await worker.start()
            #future.result()

        self.logger.log_info("Manager has started")