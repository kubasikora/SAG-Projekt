import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour


class DeputeBehaviour(OneShotBehaviour):
    async def run(self):
        print("Manager Starts")
        msg = Message(to="receiver@localhost")     # Instantiate the message
        msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
        msg.body = "Hello World {}".format(self.counter) # Set the message content
        await self.send(msg)
        print("Message sent!")

    async def on_end(self):
        # stop agent from behaviour
        await self.agent.stop()    



class ManagerAgent(Agent):


    async def setup(self):
        fsm = NegotiateFSMBehaviour)
        fsm.add_state(name=STATE_INIT, state=StateInitial(self), initial=True)
        self.add_behaviour(fsm)