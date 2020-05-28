from spade.behaviour import PeriodicBehaviour
from agents import ManagerAgent
from spade.message import Message
from math import floor

PERIOD = 10


class ControlSubordinatesBehaviour(PeriodicBehaviour):
    def __init__(self, agent, period, startTime, subordinates):
        super().__init__(period=period, start_at=startTime)
        self.manager = agent 
        self.subordinates = dict((subordinate, 0) for subordinate in subordinates) #counter how many times a subordinate didn't respond

    async def on_start(self):
        for sub in self.subordinates.keys():
            self.subordinates[sub] = 0 # if the bahaviour was restarted

    def checkResponses(self, responded):
        toRestart = []
        for sub in self.subordinates.keys():
            if sub not in responded or self.subordinates[sub] > 1:
                toRestart.append(sub)
                self.subordinates[sub] = 0
       


    async def run(self):
        #send messages to subordinates and wait to get response from each of them 
        for sub in self.subordinates.keys():
            self.manager.logger.log_warning(f"Pinging {sub}")
            msg = Message(to=sub)
            msg.set_metadata("conversation-id", "watchdog")
            msg.set_metadata("performative", "inform")
            msg.body=str(self.subordinates[sub])
            await self.send(msg)
        currentWorking = []
        timeout = floor(float(len(self.subordinates)) / PERIOD) - 1 
        if timeout < 1:
            timeout = timeout + 1
        for i in range(len(self.subordinates)):
            resp = await self.receive(timeout=timeout)
            if resp is None:
                self.manager.logger.log_warning("No response!")
            else:
                currentWorking.append(str(resp.sender))
                if resp.body == str(WorkingState.RESTARTING):
                    self.subordinates[resp.sender] = self.subordinates[resp.sender] + 1
                    self.manager.logger.log_warning(f"Restarting {resp.sender}")
                else:
                    self.subordinates[resp.sender] = 0
        toRestart = self.checkResponses(currentWorking)
        # to do !!! how to restart the whole agent? 
        
                


        