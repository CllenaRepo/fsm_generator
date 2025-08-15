class FiniteStateMachine:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.current_state = None
        self.initial_state = None
        self.accept_states = set()

    def add_state(self, state, is_accept=False):
        """Add a state to the FSM."""
        self.states.add(state)
        if is_accept:
            self.accept_states.add(state)
        if not self.initial_state:
            self.initial_state = state
            self.current_state = state

    def add_transition(self, from_state, event, to_state):
        """Add a transition from one state to another on a given event."""
        if from_state not in self.states or to_state not in self.states:
            raise ValueError("Both states must exist in the FSM")
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][event] = to_state

    def process_event(self, event):
        """Process an event and transition to the next state if valid."""
        if self.current_state not in self.transitions:
            raise ValueError(f"No transitions defined for state {self.current_state}")
        if event not in self.transitions[self.current_state]:
            raise ValueError(f"No transition defined for event {event} in state {self.current_state}")
        self.current_state = self.transitions[self.current_state][event]
        return self.current_state

    def get_current_state(self):
        """Return the current state of the FSM."""
        return self.current_state

    def is_accept_state(self):
        """Check if the current state is an accept state."""
        return self.current_state in self.accept_states

    def reset(self):
        """Reset the FSM to the initial state."""
        self.current_state = self.initial_state

def create_modthree_fsm():
    fsm = FiniteStateMachine()
    
    # Define states
    fsm.add_state("locked", is_accept=True)
    fsm.add_state("unlocked")
    
    # Define transitions
    fsm.add_transition("locked", "push", "locked")
    fsm.add_transition("locked", "coin", "unlocked")
    fsm.add_transition("unlocked", "push", "locked")
    fsm.add_transition("unlocked", "coin", "unlocked")
    
    return fsm

if __name__ == "__main__":
    # Create and test a sample FSM (e.g., a turnstile)
    fsm = create_sample_fsm()
    
    print(f"Initial state: {fsm.get_current_state()}")
    
    # Test some transitions
    try:
        print("Processing event: coin")
        new_state = fsm.process_event("coin")
        print(f"New state: {new_state}, Is accept state? {fsm.is_accept_state()}")
        
        print("Processing event: push")
        new_state = fsm.process_event("push")
        print(f"New state: {new_state}, Is accept state? {fsm.is_accept_state()}")
        
        print("Processing event: coin")
        new_state = fsm.process_event("coin")
        print(f"New state: {new_state}, Is accept state? {fsm.is_accept_state()}")
        
        # Reset to initial state
        fsm.reset()
        print(f"After reset, state: {fsm.get_current_state()}")
        
        # Test invalid event
        print("Processing invalid event: invalid")
        fsm.process_event("invalid")
    except ValueError as e:
        print(f"Error: {e}")