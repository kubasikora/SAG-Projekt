from spade.behaviour import PeriodicBehaviour
from agents import FactoryAgent
from spade.message import Message
from enum import Enum

PERIOD = 10

class WorkingState(Enum):
    OK = 1
    RESTARTING = 2

class WatchdogBehaviour(PeriodicBehaviour):
    def __init__(self, agent, period, startTime):
        super().__init__(period=period, start_at=startTime)
        self.fAgent = agent         

    async def on_start(self):
        self.counter = 0 #counter which will be used to "monitor" manager

    def checkState(self):
        toRet = WorkingState.OK
        for behaviour in self.fAgent.behaviours:
            if behaviour.is_killed():
                behaviour.start()
                self.manager.logger.log_error("Behaviour {str(behaviour)} killed")
                toRet = WorkingState.RESTARTING
        return toRet

    async def run(self):
        #wait for message from your boss
        timeout = PERIOD -1
        msg = await self.receive(timeout=timeout)
        if msg is None:
            self.counter = self.counter + 1
        else:
            self.counter = 0
            resp = Message(to=str(msg.sender))
            resp.set_metadata("conversation-id", "watchdog")
            resp.set_metadata("performative", "inform")
            resp.body = str(self.checkState())
            await self.send(resp)
        if self.counter > 1:
            self.fAgent.logger.log_error("Manager does not work!!")
            # to do handle manager not working




        