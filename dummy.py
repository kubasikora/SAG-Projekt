import time
import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class DummyAgent(Agent):
    class MyBehaviour(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour")
            self.counter = 0

        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            await asyncio.sleep(1)

    async def setup(self):
        print("Hello world! I'm agent {}".format(str(self.jid)))
        b = self.MyBehaviour()
        self.add_behaviour(b)

if __name__ == "__main__":
    dummy = DummyAgent("me@localhost", "12345678")
    dummy.start()
    dummy.web.start(hostname="localhost", port="10000")

    print("Wait until user interrupts with ctrl+C")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    dummy.stop()
