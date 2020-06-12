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
    
class Cars:
    def __init__(self, features_number):
        self.cars = []
        self.agents_number = features_number
        self.features = [Color, Engine, Body]
        self.init_cars()

    def init_cars(self):

        if self.agents_number > len(self.features):
            print("Not enough car features")
        else:
            self.features = self.features[:self.agents_number]
            self.cars = list(itertools.product(*self.features))

        
    def get_cars_amount(self):
        return len(self.cars)

    def get_cars(self):
        return self.cars

    def get_same_indexes(self, i):
        lists = [[],[],[]]

        index = 0
        for feature in self.features[i]:
            for j in range(0, len(self.cars)):
                if(self.cars[j][i] == feature):
                    lists[index].append(j)

            index = index + 1

        return [lists[0], lists[1], lists[2]]

