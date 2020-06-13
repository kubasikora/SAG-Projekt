from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from behaviours.WatchdogBehaviour import WorkingState
from messages import WatchdogMessage, StatesMessage
from math import floor
from agents import FactoryAgent

PERIOD = 10

class ControlSubordinatesBehaviour(PeriodicBehaviour):
    def __init__(self, agent, period, startTime, subordinates):
        PeriodicBehaviour.__init__(self, period=period, start_at=startTime)
        self.manager = agent 
        self.subordinates = dict((subordinate, 0) for subordinate in subordinates) #counter how many times a subordinate didn't respond
        self.manager.logger.log_info("ControlSubordinatesBehaviour created")

    async def on_start(self):
        for sub in self.subordinates.keys():
            self.subordinates[sub] = 0 # if the bahaviour was restarted

    def checkResponses(self, responded, toRestart):
        for sub in self.subordinates.keys():
            if sub not in responded:
                self.subordinates[sub] = self.subordinates[sub] + 1
            if self.subordinates[sub] > 2:
                if(sub not in toRestart):
                    toRestart.append(sub)
                self.subordinates[sub] = 0
    
    async def run(self):
        #send messages to subordinates and wait to get response from each of them 
        for sub in self.subordinates.keys():
            self.manager.logger.log_warning(f"Pinging {sub}")
            msg = WatchdogMessage(to=sub, body=self.subordinates[sub])
            await self.send(msg)

        currentWorking = []
        toRestart = []
        timeout = floor(float(PERIOD) / len(self.subordinates)) - 1 
        if timeout < 1:
            timeout = timeout + 1
        for i in range(len(self.subordinates)):
            resp = await self.receive(timeout=timeout)
            if resp is None:
                self.manager.logger.log_warning("No response!")
            else:
                self.manager.logger.log_warning("Ping responded!")
                if str(WorkingState.COMPLAINT) in resp.body:
                    badAgentJID = resp.body.split(" ")[1]
                    toRestart.append(badAgentJID)
                else:
                    currentWorking.append(str(resp.sender))
                    if resp.body == str(WorkingState.RESTARTING):
                        self.subordinates[str(resp.sender)] = self.subordinates[str(resp.sender)] + 1
                        self.manager.logger.log_warning(f"Restarting {resp.sender}")
                    else:
                        self.subordinates[str(resp.sender)] = 0
        self.checkResponses(currentWorking, toRestart)
        for jid in toRestart:
            worker, i = self.manager.findWorker(jid)
            await worker.stopAllBehaviours()
            p = self.manager.workersParams[i]
            self.agent.logger.log_info(f"Adding {jid} to the team")
            created = FactoryAgent.FactoryAgent(p["jid"], p["password"],p["name"],p["priceEle"], p["priceChan"], p["sameIndex"],p["coworkers"], "manager@localhost")
            self.manager.workers[i] = created
            await created.start()
            created.web.start(hostname="localhost", port="10000")
            self.agent.logger.log_info(f"DeputeBehaviour for {jid} created")
            msg = StatesMessage(to=jid, body=self.manager.task)
            msg.set_metadata("performative", "request")     # Instantiate the message
            await self.send(msg)
            self.agent.logger.log_info(f"Task sent to {jid}")

        
                


        