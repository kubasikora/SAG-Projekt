from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
import ast
#import metadata
import itertools

"""
    Klasa reprezentujaca stan poczatkowy 
    oczekuje ona na pojawienie sie wiadomosci od Managera
    nastepnie oblicznae jest B0prim oraz najgorsza mozliwa wartosc
"""
class StateInitial(State):
    def __init__(self, agent):
        #super(StateInitial).__init__(self)
        self.agent = agent

    """
        Algorytm obliczajacy najgorszy mozliwy koszt jaki dany agent moze wygenerowac
        na samym poczatku obliczane jest ile nalezy wyprodukowac produktow z tej samej grupy
        kolejno sprawdza sie ile maksymalnie mozna dokonac zmian (ktore generuja dodatkow koszty)
    """

    def computeWorst(self, itemA, itemB, itemC, priceChange, priceEach):
        sumEle = itemA + itemB + itemC
        cost = sumEle * priceEach
        lastT = "n"
        nextT = "n"
        while(sumEle > 0):
            mapEle = { "a": itemA, "b": itemB, "c": itemC}
            mapsSorted = sorted(mapEle.items(), key = lambda x: x[1])
            if mapsSorted[0][0] != lastT or mapsSorted[1][1] == 0:
                nextT = mapsSorted[0][0]
            elif mapsSorted[1][0] != lastT or mapsSorted[2][1] == 0:
                nextT = mapsSorted[1][0]
            else:
                nextT = mapsSorted[2][0]

            sumEle = sumEle -1

            if nextT != lastT:
                cost = cost + priceChange
            lastT = nextT
            if nextT =="a":
                itemA = itemA -1
            elif nextT == "b":
                itemB = itemB -1
            else:
                itemC = itemC -1
        
        if(nextT != "n"):
            cost = cost - priceChange #needed to get rid of initial cos (as the algorith consider first item as change)
        return cost
    """
        Funkcja bedaca proxy do obliczania najwiekszego mozliwego kosztu
    """
    def getWorst(self, resp):
        pricePerPiece = agent.getPricePerPiece()
        pricePerChange = agent.getPricePerChange()
        indexes = agent.getSameIndexes()
        first = 0
        second = 0
        third = 0
        for index1 in indexes[0]:
            first = first + resp[index1]
        for index2 in indexes[1]:
            second = second + resp[index2]
        for index3 in indexes[2]:
            third = third + resp[index3]
        return self.computeWorst(first, second, third, pricePerChange, pricePerPiece)
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
        lista = []
        for i in indexes:
            suma = suma + resp[i]
            for k in resp[i]:
                lista.append(i)
        allPerm = list(itertools.permutations(lista))
        return self.removeDuplicats(allPerm)

        #We should have suma! different 
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
        indexes = agent.getSameIndexes() 
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
        print("Starting state init: agent "+self.agent.getName())
        self.agent.clearTable()
        msg = await self.receive(timeout=30) 
        print("I got msg! "+msg.body)
        if (msg is not None):
            print("good msg")
            print ("typ wiadomosci " + type(msg.body).__name__)
            #res = json.loads(msg.body)
            res = ast.literal_eval(msg.body)
            print("Wanted: "+ res)
            self.agent.setToProduce(res)
            worst = self.getWorst(res)
            if worst == 0 :
                print("empty order")
            else:
                print("the worst i can get "+worst+" my name "+self.agent.getName())
                self.agent.setWorst(worst)
                B0prim = self.createB0prim(res)
                self.agent.setB0prim(B0prim)
                #self.set_next_state(STATE_COMPUTE_B0)                              proper next step!!
                       

