from spade.message import Message 
from spade.behaviour import State
from agents import FactoryAgent
from .metadata import *
from copy import deepcopy


#sprawdzanie czy dokonano dealu 
class StateComputeProposals(State):
    
    def __init__(self, agent):
        super().__init__()
        self.fAgent = agent
    
    def decide(self, myAgree, myDisagree, limit):
        for co in self.fAgent.activeCoworkers:
            proposition = self.fAgent.matesProposals[co][len(self.fAgent.matesProposals[co])-1]            
            if limit >= self.fAgent.getMyCost(str(proposition), proposition):
                myAgree[co] = proposition
                self.fAgent.logger.log_success("I agree")
            else:
                myDisagree[co] = proposition


    def checkFinalResultInSaved(self, waitingCoworkers , agreementFound):
      
        toRemove = []
        for msg in self.fAgent.mailboxForLater:
            if msg.metadata["performative"] == "confirm":
                agreementFound = True
                toRemove.append(msg)
                waitingCoworkers.remove(str(msg.sender))
            elif msg.metadata["performative"] == "disconfirm":
                toRemove.append(msg)
                waitingCoworkers.remove(str(msg.sender))
        for msg in toRemove:
            self.fAgent.mailboxForLater.remove(msg)
        return agreementFound

       

    async def run(self):
        self.fAgent.logger.log_info("Starting computing proposals")
        myAgree = dict()
        myDisagree = dict()
        sigma = self.fAgent.currentSigma
        worstProposed = self.fAgent.myWorstProposal
        limit = self.fAgent.getMyCost(str(worstProposed), worstProposed) # in the article they used utility but as utility is def as worst - cost, we can use just cost
        self.fAgent.logger.log_info(f"my limit is {limit}")
        #compute your decision (if you agree or disagree)
        self.decide(myAgree,myDisagree,limit)

        # send it to coworkers
        for co, sigma in myAgree.items():
            msg = Message(to=co)
            msg.set_metadata("performative", "accept-proposal")
            msg.set_metadata("conversation-id", "1") #here an error occured -> the agent got message too early
            msg.body = "ok"
            await self.send(msg)
        for co, sigma in myDisagree.items():
            msg = Message(to=co)
            msg.set_metadata("performative", "reject-proposal")
            msg.set_metadata("conversation-id", "1") #here an error occured -> the agent got message too early
            msg.body = "not ok"
            await self.send(msg) 


        #check if others agree with your proposal
        waitingCoworkers = deepcopy(self.fAgent.activeCoworkers)
        ok = 0
        nok = 0
        while (len(waitingCoworkers) > 0):
            msg = await self.receive(timeout = 5)
            if msg is not None:
                sender = str(msg.sender)
                if msg.metadata["performative"] == "accept-proposal":
                    waitingCoworkers.remove(sender)
                    ok = ok +1
                elif msg.metadata["performative"] == "reject-proposal":
                    waitingCoworkers.remove(sender)
                    nok = nok +1
                else:
                    self.fAgent.saveMessage(msg)
    
        self.fAgent.logger.log_info(f"I've got {ok} oks and {nok} not oks")
        agreementFound = False
        if nok == 0:
            self.fAgent.logger.log_success("Agreement found!!")
            body = str(sigma)
            perf = "confirm"
            agreementFound = True
        else: 
            perf = "disconfirm"
            body = ""
            self.fAgent.logger.log_warning("Need to work more")

        # notify other if there is or there is not an agreement
        for co in self.fAgent.activeCoworkers:
            msg = Message(to=co)
            msg.set_metadata("performative", perf)
            msg.set_metadata("conversation-id", "1") #here an error occured -> the agent got message too early
            msg.body = body
            await self.send(msg)      
           
        # check if there other agents proposal is correct 
        
        waitingCoworkers = deepcopy(self.fAgent.activeCoworkers)     

        agreementFound = self.checkFinalResultInSaved(waitingCoworkers,agreementFound)

        while (len(waitingCoworkers)> 0 and agreementFound == False):
            msg = await self.receive(timeout = 5)
            if msg is not None:
                sender = str(msg.sender)
                if msg.metadata["performative"] == "confirm":
                    waitingCoworkers.remove(sender)
                    agreementFound = True
                elif msg.metadata["performative"] == "disconfirm":
                    waitingCoworkers.remove(sender)
                else:
                    self.fAgent.saveMessage(msg)

        if agreementFound == True:
            self.fAgent.logger.log_success("The end")
            self.fAgent.logger.log_success(f"The cost {self.fAgent.getCostAll(str(self.fAgent.currentSigma))}")
            self.fAgent.logger.log_success(f"Winning sequence {self.fAgent.currentSigma}")
            # print(min(self.fAgent.allCalculatedCosts.values()))
            for co in self.fAgent.coworkers:
                msg = Message(to=co)
                msg.set_metadata("performative", "inform")
                msg.set_metadata("conversation-id", "1") #here an error occured -> the agent got message too early
                msg.body = "We have got it!"
                await self.send(msg) 
            self.set_next_state(STATE_NOT_ACTIVE)

        else:
            self.set_next_state(STATE_COMPUTE_RISK)
            




        



