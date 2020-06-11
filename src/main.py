from agents import FactoryAgent , ManagerAgent
from Cars import *
from Logger import Logger
import time, sys, os
from spade.agent import Agent


if __name__ == "__main__":
    logger = Logger("main")
    logger.log_info("Start")
    dictTest={0:0, 1:0, 2:0, 3:4, 4:0, 5:7, 6:7, 7:8, 8:0, 9:0 , 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:9, 17:5, 18:0, 19:0, 20:1, 21:9, 22:3, 23:0, 24:0, 25:6, 26:0}

    #to do create in cars (or somewhere else) params form more than 3 agents -> the rest of algorith should stay the same (remember to create jid's in prosodyctl)
    painterPar={"jid": "paintera@localhost", "password": "12345678", "name":"PainterA" , "priceEle":5 , "priceChan":5, "sameIndex":getSameIndexesColors() , "coworkers": ["assemblya@localhost", "weldera@localhost"]}
    welderPar={"jid":"weldera@localhost" , "password": "12345678", "name":"WelderA" , "priceEle":5, "priceChan": 5,"sameIndex":getSameIndexesBody() , "coworkers": ["assemblya@localhost", "paintera@localhost"]}
    assemblyPar={"jid": "assemblya@localhost", "password": "12345678", "name": "AssemblyA", "priceEle":5, "priceChan": 5,"sameIndex":getSameIndexesEngine() , "coworkers":["weldera@localhost", "paintera@localhost"] }

    params = [painterPar,welderPar, assemblyPar ]

    managerAgent = ManagerAgent("manager@localhost", "12345678",params, dictTest)
    managerAgent.start()
    managerAgent.web.start(hostname="localhost", port="10001")

    while True:
        try:
            time.sleep(1)
            if managerAgent.waitForOptimalSequence.is_killed():
                break
        except KeyboardInterrupt:
            managerAgent.stop()
            break

    logger.log_info("Agents finished")
    os._exit(0)