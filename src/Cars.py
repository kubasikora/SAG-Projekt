from enum import Enum

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
    def __init__(self, col, eng, bod):
        self.color = col
        self.engine = eng
        self.body = bod
    def getColor(self):
        return self.color
    def getEngine(self):
        return self.engine
    def getBody(self):
        return self.body


color = [Color.RED, Color.GREEN, Color.BLUE]
engine = [Engine.DIESEL, Engine.PETROL, Engine.ELECTRIC]
body = [Body.LIMO, Body.ESTATE, Body.HATCHBACK]

cars = []

for co in color:
    for en in engine:
        for bo in body:
            cars.append(Car(co,en,bo))

def getCars():
    return cars


def getSameIndexesColors():
    colRed = []
    colGreen = []
    colBlue = []
    for i in range(len(cars)):
        if cars[i].getColor() == Color.RED:
            colRed.append(i)
        elif cars[i].getColor == Color.GREEN:
            colGreen.append(i)
        else:
            colBlue.append(i)
    return [colRed, colBlue, colGreen]

def getSameIndexesEngine():
    enDie = []
    enPe = []
    enEl = []
    for i in range(len(cars)):
        if cars[i].getEngine() == Engine.DIESEL:
            enDie.append(i)
        elif cars[i].getEngine() == Engine.PETROL:
            enPe.append(i)
        else:
            enEl.append(i)
    return [enDie, enPe, enEl]

def getSameIndexesBody():
    boLi =[]
    boEs = []
    boHa = []
    for i in range(len(cars)):
        if cars[i].getBody() == Body.LIMO:
            boLi.append(i)
        elif cars[i].getBody() == Body.ESTATE:
            boEs.append(i)
        else:
            boHa.append(i)
    return [boLi, boEs, boHa]
