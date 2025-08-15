"""This code is a Finite State Machine (FSM) generator with a modulo three FSM for show and testing."""

from typing import Optional, Iterable

class FiniteStateMachine:
    def __init__(self):
        self.states = set()
        self.state_values = {}
        self.alphabet = set()
        self.transitions = {}
        self.current_state = None
        self.initial_state = None
        self.accept_states = set()

    def add_state(self, state_name: str, is_accept: bool = False) -> None:
        """ Adds a state to the FSM.

            Args:
                state_name (str): The name of the state to add.
                is_accept (bool): Whether the state is an accepting state.

            Returns:
                None
        """

        self.states.add(state_name)
        if is_accept:
            self.accept_states.add(state_name)
        if not self.initial_state:
            self.initial_state = state_name
            self.current_state = state_name

    def add_state_value(self, state: str, state_value: Optional[int] = None) -> None:
        """Map a state to its value.
        
            Args:
                state (str): The name of the state.
                state_value (int, optional): the value that the state represents in the FSM.

            Raises:
                ValueError: If we're adding a value to a state that doesn't exist.

            Returns:
                None
        """

        if state not in self.states:
            raise ValueError("State must exist in the states set.")

        self.state_values[state] = state_value

    def add_alphabet(self, alphabet: Iterable) -> None:
        """Adds an entire alphabet system to the FSM.

            Args:
                alphabet (iterable): an entire set of alphabet.

            Raises:
                ValueError: Alphabet must exist.

            Returns:
                None
        """

        if alphabet is None or len(alphabet) == 0:
            raise ValueError("Alphabet must exist.")

        self.alphabet = set(alphabet)

    def add_transition_function(self, from_state: str, event, to_state: str) -> None:
        """Add a transition function from one state to another on a given event.
        
            Args:
                from_state (str): The state we're transitioning from.
                event: The cause for transitioning into another state.
                to_state (str): The state we're transitioning to.

            Raises:
                ValueError: If the state we're transitioning to/from doesn't exist or if the event isn't in the alphabet set. 

            Returns:
                None
        """

        if from_state not in self.states or to_state not in self.states:
            raise ValueError("Both states must exist in the FSM.")
        if event not in self.alphabet:
            raise ValueError("Event must exist in the alphabet set.")

        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        self.transitions[from_state][event] = to_state

    def process_event(self, event) -> str:
        """Process an event and transition to the next state if valid.
        
            Args:
                event: The cause for transitioning into another state.

            Raises:
                ValueError: If the event isn't in the alphabet set or if the state/event doesn't have any transitions.  

            Returns:
                The current state.
        """

        if self.current_state not in self.transitions:
            raise ValueError(f"No transitions defined for state {self.current_state}")
        if event not in self.alphabet:
            raise ValueError(f"Event {event} is invalid")           
        if event not in self.transitions[self.current_state]:
            raise ValueError(f"No transition defined for event {event} in state {self.current_state}")

        self.current_state = self.transitions[self.current_state][event]
        return self.current_state

    def get_current_state(self) -> str:
        """Return the current state of the FSM.
        
            Args:
                None

            Returns:
                The current state.
        """

        return self.current_state

    def get_current_state_value(self) -> int:
        """Return the current final state of the FSM.
        
            Args:
                None

            Raises:
                ValueError: If the state values isn't instantiated or defined.

            Returns:
                The value of the current state.
        """

        if len(self.state_values) == 0:
            raise ValueError("No final states instantiated.")
        if self.current_state not in self.state_values:
            raise ValueError(f"No final value defined for state {self.current_state}")

        return self.state_values[self.current_state]

    def is_accept_state(self) -> bool:
        """Check if the current state is an accepting state.
        
            Args:
                None

            Returns:
                True if the current state we're in is an accepting state, False otherwise.
        """

        return self.current_state in self.accept_states


def create_mod_three_fsm() -> FiniteStateMachine:
    """Creates a ModThree FSM.
    
        Args: 
            None

        Returns: 
            A FiniteStateMachine object representing a ModThree FSM.
    """

    fsm = FiniteStateMachine()
    
    # Define states
    fsm.add_state("S0", is_accept=True)
    fsm.add_state("S1", is_accept=True)
    fsm.add_state("S2", is_accept=True)

    # Define state values
    fsm.add_state_value("S0", 0)
    fsm.add_state_value("S1", 1)
    fsm.add_state_value("S2", 2)

    # Define alphabet
    fsm.add_alphabet({"0", "1"})

    # Define transition functions
    fsm.add_transition_function("S0", "0", "S0")
    fsm.add_transition_function("S0", "1", "S1")

    fsm.add_transition_function("S1", "0", "S2")
    fsm.add_transition_function("S1", "1", "S0")

    fsm.add_transition_function("S2", "0", "S1")
    fsm.add_transition_function("S2", "1", "S2")
    
    return fsm

def mod_three(input_str: str) -> int:
    """Run a string input representing an unsigned binary integer against a ModThree FSM.
    
        Args: 
            input_str (str): A string that should only have '0' and '1' characters.

        Raises:
            ValueError: If the input contains invalid characters.    

        Returns: 
            The remainder when the input is divided by three.        
    """

    if input_str is None or len(input_str) == 0:
        raise ValueError("Invalid input.")

    fsm = create_mod_three_fsm()

    if not all(c in fsm.alphabet for c in input_str):
        raise ValueError("Input must contain only '0' or '1'.")

    for character in input_str:
        fsm.process_event(character)
    
    return fsm.get_current_state_value()


if __name__ == "__main__":
    try:
        #Some quick tests, the official testing is done at Test_FSM_Generator.py
        print(mod_three("1101"))
        print(mod_three("1110"))
        print(mod_three("1111"))
        print(mod_three(""))
        print(mod_three(None))
        print(mod_three("loremipsum"))
        print(mod_three("0"))
        print(mod_three("1"))
    except ValueError as e:
        print(f"Error: {e}")