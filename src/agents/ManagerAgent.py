import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template
from Logger import Logger
import json
import asyncio

class DeputeBehaviour(OneShotBehaviour):
    def __init__(self, agent, jidToSend):
        super().__init__()
        self.agent = agent
        self.jidToSend = jidToSend

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
        # stop agent from behaviour
        # await self.agent.stop()    
        self.kill()

class ReceiveResultBehaviour(CyclicBehaviour):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    async def run(self):
        message = await self.receive(timeout=1)
        if message is not None:
            result = json.loads(message.body)
            self.agent.logger.log_success(f"Got optimal sequence {result['sequence']} with total cost of {result['cost']}")
            self.kill()
            
    async def on_end(self):
        await self.agent.stop()

class ManagerAgent(Agent):
    async def setup(self):
        self.logger = Logger(self.jid)

        self.painterA = DeputeBehaviour(self, "paintera@localhost")
        self.add_behaviour(self.painterA)

        self.welderA = DeputeBehaviour(self, "weldera@localhost")
        self.add_behaviour(self.welderA)

        self.assemblyA = DeputeBehaviour(self, "assemblya@localhost")
        self.add_behaviour(self.assemblyA)

        self.waitForOptimalSequence = ReceiveResultBehaviour(self)
        receiver_template = Template()
        receiver_template.set_metadata("performative", "inform")
        receiver_template.set_metadata("conversation-id", "results")
        self.add_behaviour(self.waitForOptimalSequence, receiver_template)
        
        self.logger.log_info("Manager has started")