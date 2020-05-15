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
        dictTest={0:1, 1:2, 2:3, 3:2, 4:0, 5:1, 6:2, 7:3, 8:4, 9:4 , 10:5, 11:6, 12:7, 13:8, 14:9, 15:0, 16:0, 17:1, 18:1, 19:2, 20:2, 21:1, 22:0, 23:9, 24:1, 25:1, 26:9}
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