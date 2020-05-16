from agents import FactoryAgent , ManagerAgent
from Cars import *
import time
from spade.agent import Agent


if __name__ == "__main__":
    print("Start")
    painterAAgent = FactoryAgent("painterA@localhost", "12345678","PainterA",5, 5, getSameIndexesColors(),["assemblyA@localhost", "welderA@localhost"])
    future = painterAAgent.start()
    painterAAgent.web.start(hostname="localhost", port="10000")
    future.result()

    welderAAgent = FactoryAgent("welderA@localhost", "12345678","WelderA",5, 5, getSameIndexesBody(),["assemblyA@localhost", "painterA@localhost"])
    future2 = welderAAgent.start()
    welderAAgent.web.start(hostname="localhost", port="10000")
    future2.result()

    assemblyAAgent = FactoryAgent("assemblyA@localhost", "12345678","AssemblyA",5, 5, getSameIndexesEngine(),["welderA@localhost", "painterA@localhost"])
    future3 = assemblyAAgent.start()
    assemblyAAgent.web.start(hostname="localhost", port="10000")
    future3.result()


    managerAgent = ManagerAgent("manager@localhost", "12345678")
    managerAgent.start()
    managerAgent.web.start(hostname="localhost", port="10001")


    while 1:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            painterAAgent.stop()
            managerAgent.stop()
            break

    print("Agents finished")