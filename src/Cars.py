from enum import Enum
import itertools


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Engine(Enum):
    DIESEL = 1
    PETROL = 2
    ELECTRIC =3

class Body(Enum):
    LIMO = 1
    ESTATE = 2
    HATCHBACK = 3

class TypeA(Enum):
    TYPEA_1 = 1
    TYPEA_2 = 2
    TYPEA_3 = 3

class TypeB(Enum):
    TYPEB_1 = 1
    TYPEB_2 = 2
    TYPEB_3 = 3

class TypeC(Enum):
    TYPEC_1 = 1
    TYPEC_2 = 2
    TYPEC_3 = 3  

class Car:
    def __init__(self):
        self.features = []
    def setFeature(self, i, value):
        self.features[i] = value
    def getFeature(self, i):
        return self.features[i]
    def __repr__(self):
        string = ''
        for feature in self.features:
            string = string + str(feature) + ' '
        return string
    
cars = []

def init_cars(agents_number):

    features = [Color, Engine, Body, TypeA, TypeB, TypeC]

    if agents_number > len(features):
        '''

        '''
        print("Not enough car features")
        return
    else:
        '''
        
        '''
        features = features[:agents_number]

    cars = list(itertools.product(*features))

    return len(cars), cars

def getCars():
    return cars

def getSameIndexes(cars, agentNumber, i):
    features = [Color, Engine, Body]
    features = features[:agentNumber]
    lists = [[],[],[]]
    index = 0
 
    index = 0
    for feature in features[i]:
        for j in range(0, len(cars)):
            if(cars[j][i] == feature):
                #print(str(feature) + " " + str(cars[j]) + " " + str(j))
                lists[index].append(j)

        index = index + 1

    #print(lists)
    return [lists[0], lists[1], lists[2]]

