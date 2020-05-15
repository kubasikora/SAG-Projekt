import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message




class DeputeBehaviour(OneShotBehaviour):
    async def run(self):
        print("Manager Starts")
        msg = Message(to="painterA@localhost")     # Instantiate the message
        msg.set_metadata("performative", "request")  # Set the "inform" FIPA performative
        msg.set_metadata("language","dictionary" )
        dictTest={0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:3, 8:4, 9:4 , 10:0, 11:6, 12:0, 13:0, 14:9, 15:0, 16:0, 17:1, 18:0, 19:2, 20:0, 21:0, 22:0, 23:9, 24:0, 25:0, 26:9}
        msg.body = str(dictTest)
        await self.send(msg)
        print("Message sent!")

    async def on_end(self):
        # stop agent from behaviour
        await self.agent.stop()    



class ManagerAgent(Agent):

    async def setup(self):
        self.b = DeputeBehaviour()
        self.add_behaviour(self.b)