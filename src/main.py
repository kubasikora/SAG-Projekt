from agents import FactoryAgent , ManagerAgent
from Cars import *
from Logger import Logger
import time, sys, os
from spade.agent import Agent
import json
import random


def get_cooworkers(agents_jid, current_agent_index):
    index = 0
    cooworkers = []
    for agent_jid in agents_jid:
        if(index != current_agent_index):
            cooworkers.append(agent_jid)

        index = index + 1

    return cooworkers

def generate_agents_manager(data, order_dict):
    agent_number = data[test_case_order_dict]["agent_number"]
    car_manager = Cars(agent_number)
    number_of_cars = car_manager.get_cars_amount()
    
    order_dict = {}
    for i in range(0, number_of_cars):
        order_dict[i] = data[test_case_order_dict]["car_types"][i]

    agents = []
    agents_name = []
    index = 0
    
    agents_jid = []
    for agent in data["agents"]:
        if(index >= agent_number):
            break
        agents_jid.append(agent["jid"])
        index = index+1

    index = 0
    for agent in data["agents"]:
        
        if(index >= agent_number):
            break

        agent_dict = {}
        agent_dict = agent
        agent_dict["sameIndex"] = car_manager.get_same_indexes(index)
        agent_dict["coworkers"] = get_cooworkers(agents_jid, index)

        agents.append(agent_dict)
        index = index + 1

    manager_name = data["maganer"]["jid"]
    manager_password = data["maganer"]["password"]

    managerAgent = ManagerAgent(manager_name, manager_password, agents, order_dict)
    return managerAgent, agent_number

if __name__ == "__main__":
    logger = Logger("main")
    logger.log_info("Start")

    with open("config/agents.config.json", "r") as read_file:
        data = json.load(read_file)
        

    if len(sys.argv) <= 1:
        print("No test case selected")
    else:
        test_case = int(sys.argv[1])

        if test_case == 0:
            print("Test case: 3 agents are working")
            test_case_order_dict = "order1"
            managerAgent, agent_number = generate_agents_manager(data, test_case_order_dict)
            managerAgent.start()
            managerAgent.web.start(hostname="localhost", port="10001")

        elif test_case == 1:
            print("Test case: 7 agents are working")
            
            test_case_order_dict = "order2"
            managerAgent, agent_number = generate_agents_manager(data, test_case_order_dict)
            managerAgent.start()
            managerAgent.web.start(hostname="localhost", port="10001")
            
            
        elif test_case == 2:
            print("Test case: 7 agents are working, killing one random agent")
            
            test_case_order_dict = "order2"
            managerAgent, agent_number = generate_agents_manager(data, test_case_order_dict)
            managerAgent.start()
            managerAgent.web.start(hostname="localhost", port="10001")
            time.sleep(15)
            managerAgent.workers[random.choice(range(0,agent_number))].stop()
            
            
        elif test_case == 3:
            print("Test case: 7 agents are working, killing random number of agents")
            
            test_case_order_dict = "order2"
            managerAgent, agent_number = generate_agents_manager(data, test_case_order_dict)
            managerAgent.start()
            managerAgent.web.start(hostname="localhost", port="10001")
            time.sleep(15)
            random_number = random.choice(range(0,agent_number))
            for i in range(0, random_number):
                 managerAgent.workers[random.choice(range(0,agent_number))].stop()


        elif test_case == 4:
            print("Test case: 7 agents are working, killing all agents")
            
            test_case_order_dict = "order2"
            managerAgent,agent_number = generate_agents_manager(data, test_case_order_dict)
            managerAgent.start()
            managerAgent.web.start(hostname="localhost", port="10001")
            time.sleep(15)
            for index in range(0,agent_number):
                managerAgent.workers[index].stop()
       

        elif test_case == 5:
            print("Test case: 7 agents are working, killing random behaviour of random agent") 
        
            test_case_order_dict = "order2"
            managerAgent,agent_number = generate_agents_manager(data, test_case_order_dict)
            managerAgent.start()
            managerAgent.web.start(hostname="localhost", port="10001")
            time.sleep(15)
            # managerAgent.workers[random.choice(range(0,agent_number))]. => ???

        else:
            print("Wrong number")
            os._exit(0) 

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