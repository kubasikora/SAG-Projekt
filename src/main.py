from agents import FactoryAgent , ManagerAgent
from Cars import *
from Logger import Logger
import time, sys, os
from spade.agent import Agent


if __name__ == "__main__":
    logger = Logger("main")
    logger.log_info("Start")

    painterAAgent = FactoryAgent("paintera@localhost", "12345678","PainterA",5, 5, getSameIndexesColors(),["assemblya@localhost", "weldera@localhost"], "manager@localhost")
    future = painterAAgent.start()
    painterAAgent.web.start(hostname="localhost", port="10000")
    future.result()

    welderAAgent = FactoryAgent("weldera@localhost", "12345678","WelderA",5, 5, getSameIndexesBody(),["assemblya@localhost", "paintera@localhost"], "manager@localhost")
    future2 = welderAAgent.start()
    welderAAgent.web.start(hostname="localhost", port="10000")
    future2.result()

    assemblyAAgent = FactoryAgent("assemblya@localhost", "12345678","AssemblyA",5, 5, getSameIndexesEngine(),["weldera@localhost", "paintera@localhost"], "manager@localhost")
    future3 = assemblyAAgent.start()
    assemblyAAgent.web.start(hostname="localhost", port="10000")
    future3.result()

    managerAgent = ManagerAgent("manager@localhost", "12345678")
    managerAgent.start()
    managerAgent.web.start(hostname="localhost", port="10001")

    while True:
        try:
            time.sleep(1)
            if managerAgent.waitForOptimalSequence.is_killed():
                break
        except KeyboardInterrupt:
            painterAAgent.stop()
            welderAAgent.stop()
            assemblyAAgent.stop()
            managerAgent.stop()
            break

    logger.log_info("Agents finished")
    os._exit(0)