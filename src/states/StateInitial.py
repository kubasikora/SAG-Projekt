from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
import itertools

def string2Dict(string):
    withoutMArg = string.replace("{", "")
    withoutMArg = withoutMArg.replace("}", "")
    poles = withoutMArg.split(",")
    toReturn = dict()
    for val in poles:
        val = val.replace(" ", "")     
        pair = val.split(":")
        k = int(pair[0])
        v = int(pair[1])
        toReturn.update({k:v})
    return toReturn

"""
    Klasa reprezentujaca stan poczatkowy 
    oczekuje ona na pojawienie sie wiadomosci od Managera
    nastepnie oblicznae jest B0prim oraz najgorsza mozliwa wartosc
"""
class StateInitial(State):
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent

    """
        Algorytm obliczajacy najgorszy mozliwy koszt jaki dany agent moze wygenerowac
        na samym poczatku obliczane jest ile nalezy wyprodukowac produktow z tej samej grupy
        kolejno sprawdza sie ile maksymalnie mozna dokonac zmian (ktore generuja dodatkow koszty)
    """

    def computeWorst(self, itemA, itemB, itemC,sumEle, priceChange, priceEach):       
        cost = sumEle * priceEach
        types = itemA + itemB + itemC
        lastT = "n"
        nextT = "n"
        while(types > 0):
            mapEle = { "a": itemA, "b": itemB, "c": itemC}
            mapsSorted = sorted(mapEle.items(), key = lambda x: x[1])
            if mapsSorted[2][0] != lastT or mapsSorted[1][1] == 0:
                nextT = mapsSorted[2][0]
            elif mapsSorted[1][0] != lastT or mapsSorted[0][1] == 0:
                nextT = mapsSorted[1][0]
            else:
                nextT = mapsSorted[0][0]

            types = types -1

            if nextT != lastT:
                cost = cost + priceChange
            lastT = nextT
            if nextT =="a":
                itemA = itemA -1
            elif nextT == "b":
                itemB = itemB -1
            else:
                itemC = itemC -1
        
        if(lastT == "n"):
            cost = cost - priceChange #needed to get rid of initial cos (as the algorith consider first item as change)
        return cost
    """
        Funkcja bedaca proxy do obliczania najwiekszego mozliwego kosztu
    """
    def getWorst(self, resp):
        pricePerPiece = self.fAgent.pricePerEl
        pricePerChange = self.fAgent.pricePerChange
        indexes = self.fAgent.sameIndexes
        first = 0
        second = 0
        third = 0
        elements = 0
        for index1 in indexes[0]:
            #first = first + resp[index1] despite adding all of the elements we do not even consider splitting the same products
            elements = elements + resp[index1]
            if resp[index1] != 0:
                first = first + 1 
        for index2 in indexes[1]:
            elements = elements + resp[index2]
            if resp[index2] != 0:
                second = second + 1             
        for index3 in indexes[2]:
            elements = elements + resp[index3]
            if resp[index3] != 0:
                third = third + 1               
        return self.computeWorst(first, second, third,elements, pricePerChange, pricePerPiece)
    """
        Funkcja usuwajaca duplikaty z listy
    """
    def removeDuplicats(selt , lista):
        toReturn = []
        for i in lista:
            if i not in toReturn:
                toReturn.append(i)
        return toReturn
    """
        Funkcja tworzaca wszystkie mozliwe permutacje zbioru obiektow o danej cesze 
        na poczatku z listy wszystkich aut do stworzenia wybierane sa auta o danej cesze (na przyklad wszystkie czerwone)
        a nastepnie tworzone sa wszystkie permutacje (bez powtorzen) 
    """
    def createSubLists(self, resp, indexes):
        suma = 0
        allPermutations = []
        indexesToPerm = []
        for i in indexes:
            if resp[i] != 0:
                indexesToPerm.append(i)
        self.fAgent.logger.log_info(f"size of list to permutate {str(len(indexesToPerm))}")
        indexesPerm = list(itertools.permutations(indexesToPerm))
        for permutation in indexesPerm:
            solution = []
            for ind in permutation:
                for howmany in range(resp[ind]):
                    solution.append(ind) 
            if len(solution) > 0:           
                allPermutations.append(solution)
        return allPermutations

    """
        Konwersja elementow z listy
        Laczy liste list w jedna liste
    """
    def convertList(self, element):
        toReturn = []
        for i in element:
            for e in i:
                toReturn.append(e)
        return toReturn

    """
        Algorytm wyznaczania zbioru B0prim 
        B0prim jest optymalny (dla danego agenta), czyli minimalizuje zmiany
        Na poczatku dzielone sa obiekty wedlug cech za ktora odpowiada dany agent
        Sposrod tych podzbiorw wyznaczane sa wszystkie mozliwe permutacje
        (na przyklad permutacje wszystkich czerwonych samochodow)
        Po stowrzeniu permutacji wewnatrz danej cechy, dokonywana jest permutacja wedlug cech 
        na przyklad [wszystkie czerwone, wszystkie niebieskie, wszystkie zielone] 
        Uwaga na zbiory puste (jesli nie ma do wyprodukowania aut o danej wartosci cechy)
    """
    def createB0prim(self, items):
        indexes = self.fAgent.sameIndexes
        sublistA = self.createSubLists(items, indexes[0])
        sublistB = self.createSubLists(items, indexes[1])
        sublistC = self.createSubLists(items, indexes[2])
        
        B0prim = []
        if len(sublistA) > 0 and len(sublistB) > 0 and len(sublistC) > 0:
            for l in sublistA:
                for k in sublistB:
                    for j in sublistC:
                        elements = list(itertools.permutations([l, k, j]))
                        for el in elements:
                            B0prim.append(self.convertList(el))
        elif len(sublistA)> 0 and len(sublistB) > 0 :
            for l in sublistA:
                for k in sublistB:
                    elements = list(itertools.permutations([l, k]))
                    for el in elements:
                        B0prim.append(self.convertList(el))   
        elif len(sublistA) > 0 and len(sublistC)>0 :         
            for l in sublistA:
                for k in sublistC:
                    elements = list(itertools.permutations([l, k]))
                    for el in elements:
                        B0prim.append(self.convertList(el)) 
        elif len(sublistA) > 0 :
            for el in sublistA:
                B0prim.append(el)
        elif len(sublistB) > 0 and len(sublistC) > 0 :
            for l in sublistB:
                for k in sublistC:
                    elements = list(itertools.permutations([l, k]))
                    for el in elements:
                        B0prim.append(self.convertList(el))             
        elif len(sublistB) > 0 :
            for el in sublistB:
                B0prim.append(el)
        else:
            for el in sublistC:
                B0prim.append(el)
        return B0prim


    async def run(self):
        self.fAgent.logger.log_info(f"Starting state init: agent {self.fAgent.nameMy}")
        if len(self.fAgent.behaviours) != 0:
            self.fAgent.logger.log_error(f"fsm state = {self.fAgent.behaviours[0]}")
        
        self.fAgent.clearTables()

        msg = await self.receive(timeout=30) 
        if msg is not None:
            res = string2Dict(msg.body)       
            self.fAgent.itemsToCreate = res
            worst = self.getWorst(res)
            if worst == 0 :
                self.fAgent.logger.log_warning("empty order")
                self.set_next_state(STATE_INIT)
            else:
                self.fAgent.logger.log_info(f"the worst i can get {str(worst)}")
                self.fAgent.worst = worst

                B0prim = self.createB0prim(res)
                self.fAgent.logger.log_info(f"my Bprim size is {str(len(B0prim))}")

                self.fAgent.B0prim = B0prim
                self.fAgent.logger.log_success("Going to state compute b0")
                self.set_next_state(STATE_COMPUTE_B0)
        else:
            self.set_next_state(STATE_INIT)
                       

