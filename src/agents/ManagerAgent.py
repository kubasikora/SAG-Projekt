import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Logger import Logger



class DeputeBehaviour(OneShotBehaviour):
    def __init__(self, jidToSend):
        super().__init__()
        self.jidToSend = jidToSend

    async def run(self):
        logger = Logger("manager@localhost")
        logger.log_info("Manager starts")
        msg = Message(to=self.jidToSend)     # Instantiate the message
        msg.set_metadata("conversation-id", "1")
        msg.set_metadata("performative", "request")  # Set the "inform" FIPA performative
        msg.set_metadata("language","dictionary" )
        dictTest={0:0, 1:0, 2:0, 3:4, 4:0, 5:7, 6:7, 7:8, 8:0, 9:0 , 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:9, 17:5, 18:0, 19:0, 20:1, 21:9, 22:3, 23:0, 24:0, 25:6, 26:0}
        msg.body = str(dictTest)
        await self.send(msg)
        logger.log_info("Message sent")

    async def on_end(self):
        # stop agent from behaviour
        await self.agent.stop()    



class ManagerAgent(Agent):
    async def setup(self):
        self.painterA = DeputeBehaviour("paintera@localhost")
        self.welderA = DeputeBehaviour("weldera@localhost")
        self.assemblyA = DeputeBehaviour("assemblya@localhost")
        self.add_behaviour(self.painterA)
        self.add_behaviour(self.welderA)
        self.add_behaviour(self.assemblyA)
        self.logger = Logger(self.jid)
        self.logger.log_info("StartManager")