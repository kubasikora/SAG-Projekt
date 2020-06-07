from spade.behaviour import FSMBehaviour
from states import *

class NegotiateFSMBehaviour(FSMBehaviour):
    def __init__(self, agent):
        FSMBehaviour.__init__(self)
        self.fAgent = agent
        self.add_state(name=STATE_INIT, state=StateInitial(agent), initial=True)
        self.add_state(name=STATE_COMPUTE_B0, state=StateComputeB0(agent))
        self.add_state(name=STATE_PROPOSE, state=StatePropose(agent))
        self.add_state(name=STATE_WAIT_FOR_PROPSALS, state=StateWaitForProposals(agent))
        self.add_state(name=STATE_COMPUTE_PROPOSALS, state=StateComputeProposals(agent))
        self.add_state(name=STATE_COMPUTE_RISK, state=StateComputeRisk(agent))
        self.add_state(name=STATE_COMPUTE_CONCESSION, state=StateComputeConcession(agent))
        self.add_state(name=STATE_WAIT_FOR_NEXT_ROUND, state=StateWaitForNextRound(agent))
        self.add_state(name=STATE_NOT_ACTIVE, state=StateNotActive(agent))

        self.add_transition(source=STATE_INIT, dest=STATE_INIT)
        self.add_transition(source=STATE_INIT, dest=STATE_COMPUTE_B0)
        self.add_transition(source=STATE_COMPUTE_B0, dest=STATE_PROPOSE)
        self.add_transition(source=STATE_PROPOSE, dest=STATE_WAIT_FOR_PROPSALS)
        self.add_transition(source=STATE_WAIT_FOR_PROPSALS, dest=STATE_COMPUTE_PROPOSALS) # compute_proposals might be final if agreement found
        self.add_transition(source=STATE_COMPUTE_PROPOSALS, dest=STATE_COMPUTE_RISK)
        self.add_transition(source=STATE_COMPUTE_PROPOSALS, dest=STATE_NOT_ACTIVE)
        self.add_transition(source=STATE_COMPUTE_RISK, dest=STATE_COMPUTE_CONCESSION)
        self.add_transition(source=STATE_COMPUTE_RISK, dest=STATE_WAIT_FOR_NEXT_ROUND)
        self.add_transition(source=STATE_COMPUTE_CONCESSION, dest=STATE_WAIT_FOR_NEXT_ROUND)
        self.add_transition(source=STATE_COMPUTE_CONCESSION, dest=STATE_NOT_ACTIVE)
        self.add_transition(source=STATE_WAIT_FOR_NEXT_ROUND, dest=STATE_PROPOSE)

    async def on_start(self):
        self.fAgent.logger.log_success(f"FSM starting at initial state {self.current_state}")

    async def on_end(self):
        self.fAgent.logger.log_success(f"Finishing at state {self.current_state}")
        #await self.agent.stop()