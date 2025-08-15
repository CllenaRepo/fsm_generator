class FiniteStateMachine:
    def __init__(self):
        self.states = set()
        self.final_states = {}
        self.alphabet = set()
        self.transitions = {}
        self.current_state = None
        self.initial_state = None
        self.accept_states = set()

    def add_state(self, stateName, is_accept = False):
        """Add a state to the FSM."""

        self.states.add(stateName)
        if is_accept:
            self.accept_states.add(stateName)
        if not self.initial_state:
            self.initial_state = stateName
            self.current_state = stateName

    def add_final_state(self, state, final_state):
        """Add an alphabet to the FSM."""

        if state not in self.states:
            raise ValueError("State must exist in the states set.")

        self.final_states[state] = final_state

    def set_alphabet(self, alphabet):
        """Add an alphabet to the FSM."""

        self.alphabet = alphabet

    def add_transition_function(self, from_state, event, to_state):
        """Add a transition from one state to another on a given event."""

        if from_state not in self.states or to_state not in self.states:
            raise ValueError("Both states must exist in the FSM")
        if event not in self.alphabet:
            raise ValueError("Event must exist in the alphabet set")

        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][event] = to_state

    def process_event(self, event):
        """Process an event and transition to the next state if valid."""

        if self.current_state not in self.transitions:
            raise ValueError(f"No transitions defined for state {self.current_state}")
        if event not in self.alphabet:
            raise ValueError(f"Event {event} is invalid")           
        if event not in self.transitions[self.current_state]:
            raise ValueError(f"No transition defined for event {event} in state {self.current_state}")
        self.current_state = self.transitions[self.current_state][event]
        return self.current_state

    def get_current_state(self):
        """Return the current state of the FSM."""

        return self.current_state

    def get_curr_final_state(self):
        """Return the current final state of the FSM."""

        if len(self.final_states) == 0:
            raise ValueError(f"No final states instantiated.")
                       
        return self.final_states[self.current_state]

    def is_accept_state(self):
        """Check if the current state is an accept state."""

        return self.current_state in self.accept_states

def create_modthree_fsm():
    fsm = FiniteStateMachine()
    
    # Define states
    fsm.add_state("S0", is_accept=True)
    fsm.add_state("S1", is_accept=True)
    fsm.add_state("S2", is_accept=True)

    # Define final states
    fsm.add_final_state("S0", 0)
    fsm.add_final_state("S1", 1)
    fsm.add_final_state("S2", 2)

    # Define alphabet
    fsm.set_alphabet({"0", "1"})

    # Define transitions
    fsm.add_transition_function("S0", "0", "S0")
    fsm.add_transition_function("S0", "1", "S1")

    fsm.add_transition_function("S1", "0", "S2")
    fsm.add_transition_function("S1", "1", "S0")

    fsm.add_transition_function("S2", "0", "S1")
    fsm.add_transition_function("S2", "1", "S2")
    
    return fsm

def modThree(input):
    fsm = create_modthree_fsm()

    for character in input:
        fsm.process_event(character)
    
    return fsm.get_curr_final_state()


if __name__ == "__main__":
    try:
        print(modThree("1101"))
        print(modThree("1110"))
        print(modThree("1111"))
    except ValueError as e:
        print(f"Error: {e}")