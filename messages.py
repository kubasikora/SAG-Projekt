import time
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour, CyclicBehaviour
from spade.message import Message
from spade.template import Template


class SenderAgent(Agent):
    class InformBehav(PeriodicBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="receiver@localhost")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Hello World {}".format(self.counter) # Set the message content
            self.counter += 1
            await self.send(msg)
            print("Message sent!")

        async def on_end(self):
            # stop agent from behaviour
            await self.agent.stop()

        async def on_start(self):
            self.counter = 0

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav(period=2)
        self.add_behaviour(b)

class ReceiverAgent(Agent):
    class RecvBehav(CyclicBehaviour):
        async def on_start(self):
            print("RecvBehav running")
            self.counter = 0

        async def run(self):
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                print("Message {} received with content: {}".format(self.counter, msg.body))
                self.counter += 1
            else:
                print("Did not received any message after 10 seconds")
                self.kill()

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        self.add_behaviour(b)


if __name__ == "__main__":
    receiveragent = ReceiverAgent("receiver@localhost", "12345678")
    future = receiveragent.start()
    receiveragent.web.start(hostname="localhost", port="10000")
    future.result() # wait for receiver agent to be prepared.
    senderagent = SenderAgent("sender@localhost", "12345678")
    senderagent.start()
    senderagent.web.start(hostname="localhost", port="10001")

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break

    print("Agents finished")