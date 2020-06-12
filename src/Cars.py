from enum import Enum
import itertools


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Paint(Enum):
    METALLIC = 1
    ACRYLIC = 2
    PEARL = 3

class Engine(Enum):
    DIESEL = 1
    PETROL = 2
    ELECTRIC =3

class Body(Enum):
    LIMO = 1
    ESTATE = 2
    HATCHBACK = 3

class Capacity(Enum):
    TWO_SEATS = 1
    FIVE_SEATS = 2
    SEVEN_SEATS = 3

class DoorsNumber(Enum):
    TWO_DOORS = 1
    THREE_DOORS = 2
    FIVE_DOORS = 3

class Radio(Enum):
    NO_RADIO = 1
    ONE_DIN = 2
    TWO_DIN = 3


class EngineLocation(Enum):
    FRONT_WHEEL = 1
    REAR_WHEEL = 2
    FOUR_WHEEL = 3

class Wheel(Enum):
    STEEL = 1
    ALLOY = 2
    CHROME = 3

class AirConditioner(Enum):
    NO_AC = 1
    EXPANSION_VALVE_SYSTEM = 2
    FIXED_ORIFICE_SYSTEM = 3


class Roof(Enum):
    BASIC_ROOF = 0
    SUN_ROOF = 1
    CONVERTIBLE = 2

class Light(Enum):
    HALOGEN = 0
    LED = 1
    HID = 2

class Wiper(Enum):
    CONVENTIONAL = 0
    FLAT = 1
    HYBRID = 2

class CarMirror(Enum):
    FLAT = 0 
    SPHERICAL = 1
    ASPHERICAL = 2

class ParkingSensor(Enum):
    NO_SENSOR = 0
    ELECTROMAGNETIC = 1
    ULTRASONIC = 2


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
        self.features = [Color, Paint, Engine, Body, Capacity,DoorsNumber,Radio, EngineLocation, Wheel,AirConditioner, Roof, Light,Wiper, CarMirror, ParkingSensor]
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

