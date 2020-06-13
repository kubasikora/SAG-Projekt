from spade.behaviour import PeriodicBehaviour
from agents import FactoryAgent
from messages import WatchdogMessage
from spade.message import Message
from enum import Enum

PERIOD = 10

class WorkingState(Enum):
    OK = 1
    RESTARTING = 2
    COMPLAINT = 3 

class WatchdogBehaviour(PeriodicBehaviour):
    def __init__(self, agent, period, startTime):
        PeriodicBehaviour.__init__(self, period=period, start_at=startTime)
        self.fAgent = agent        

    async def on_start(self):
        self.counter = 0 #counter which will be used to "monitor" manager

    def checkState(self):
        toRet = WorkingState.OK
        result = self.fAgent.checkBehaviours()
        if (result == False):
            self.fAgent.logger.log_warning("Restarting")
            toRet = WorkingState.RESTARTING
        return toRet

    async def run(self):
        #wait for message from your boss
        timeout = PERIOD -1
        msg = await self.receive(timeout=timeout)
        if msg is None:
            self.counter = self.counter + 1
        else:
            self.fAgent.logger.log_warning("Got message")
            self.counter = 0
            resp = WatchdogMessage(to=msg.sender, body=self.checkState())
            await self.send(resp)

        if self.counter > 1:
            self.fAgent.logger.log_error("Manager does not work!!")
            # to do handle manager not working




        