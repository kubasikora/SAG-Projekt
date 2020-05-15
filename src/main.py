from agents import FactoryAgent , ManagerAgent
from Cars import *
import time
from spade.agent import Agent


if __name__ == "__main__":
    print("Start")
    painterAAgent = FactoryAgent("painterA@localhost", "12345678","PainterA",5, 5, getSameIndexesColors())
    future = painterAAgent.start()
    painterAAgent.web.start(hostname="localhost", port="10000")
    future.result()

    managerAgent = ManagerAgent("manager@localhost", "12345678")
    managerAgent.start()
    managerAgent.web.start(hostname="localhost", port="10001")


    while painterAAgent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break

    print("Agents finished")