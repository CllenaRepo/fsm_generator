"""Unit tests for the FiniteStateMachine class and mod_three function."""

import unittest
from FSM_Generator import FiniteStateMachine, mod_three

# I decided to use a different FSM to test the individual functions in the FiniteStateMachine class.
# The FSM here represents a subway toll booth where it has 2 states (locked, unlocked) and 2 events that can alter its state (coin, push).
class TestFiniteStateMachine(unittest.TestCase):
    def setUp(self):
        """Set up a new FSM instance for each test."""

        self.fsm = FiniteStateMachine()
        self.fsm.add_state("locked", is_accept=True)
        self.fsm.add_state("unlocked")
        self.fsm.add_alphabet({"coin", "push"})
        self.fsm.add_transition_function("locked", "coin", "unlocked")
        self.fsm.add_transition_function("unlocked", "push", "locked")
        self.fsm.add_transition_function("locked", "push", "locked")
        self.fsm.add_transition_function("unlocked", "coin", "unlocked")

    def test_add_state(self):
        """Test adding states and setting initial state."""

        fsm = FiniteStateMachine()
        fsm.add_state("test_state")
        self.assertIn("test_state", fsm.states)
        self.assertEqual(fsm.initial_state, "test_state")
        self.assertEqual(fsm.current_state, "test_state")

        # Add the state again, it shouldn't fail since it's a set that shouldn't re-add already existing entities.
        fsm.add_state("test_state")
        self.assertIn("test_state", fsm.states)
        self.assertEqual(fsm.initial_state, "test_state")
        self.assertEqual(fsm.current_state, "test_state")

        # Test adding an accepting state
        fsm = FiniteStateMachine()
        fsm.add_state("accept_state", is_accept=True)
        self.assertIn("accept_state", fsm.accept_states)
        self.assertTrue(fsm.is_accept_state())
        
    def test_add_state_value(self):
        """Test adding values to states."""

        # Adding value to an existing state
        self.fsm.add_state_value("locked", 0)
        self.assertEqual(self.fsm.state_values["locked"], 0)

        # Adding value to a state that doesn't exist
        with self.assertRaises(ValueError):
            self.fsm.add_state_value("nonexistent", 0)

    def test_add_alphabet(self):
        """Test setting an alphabet system."""

        # All values are unique
        self.fsm = FiniteStateMachine()
        self.fsm.add_alphabet({'a', 'b', 'c'})
        self.assertEqual(self.fsm.alphabet, {'a', 'b', 'c'})

        # Some values are duplicates
        self.fsm.add_alphabet({'a', 'b', 'c', 'c'})
        self.assertEqual(self.fsm.alphabet, {'a', 'b', 'c'})

        # Invalid alphabet
        with self.assertRaises(ValueError):
            self.fsm.add_alphabet({})
        with self.assertRaises(ValueError):
            self.fsm.add_alphabet(None)

    def test_add_transition_function(self):
        """Test adding transition functions."""
        
        # Valid transition functions
        self.assertIn("locked", self.fsm.transitions)
        self.assertEqual(self.fsm.transitions["locked"]["coin"], "unlocked")

        # transition to/from invalid states
        with self.assertRaises(ValueError):
            self.fsm.add_transition_function("nonexistent", "event", "locked")
        with self.assertRaises(ValueError):
            self.fsm.add_transition_function("locked", "event", "nonexistent")

        # creating a transition with no states existing
        fsm = FiniteStateMachine()
        fsm.add_alphabet({"event"})
        with self.assertRaises(ValueError):
            self.fsm.add_transition_function("nonexistent", "event", "nonexistent")      

        # creating a transition to an alphabet that doesn't exist
        fsm = FiniteStateMachine()
        fsm.add_state("S0")
        fsm.add_state("S1")
        fsm.add_alphabet({"event"})
        with self.assertRaises(ValueError):
            self.fsm.add_transition_function("S0", "nonexistent", "S1")

    def test_process_event(self):
        """Test processing valid events."""

        # Valid events
        self.assertEqual(self.fsm.get_current_state(), "locked")
        self.fsm.process_event("coin")
        self.assertEqual(self.fsm.get_current_state(), "unlocked")
        self.fsm.process_event("push")
        self.assertEqual(self.fsm.get_current_state(), "locked")

        # Invalid events
        with self.assertRaises(ValueError):
            self.fsm.process_event("invalid_event")

        # Test processing an event from a state with no transitions.
        fsm = FiniteStateMachine()
        fsm.add_state("isolated")
        fsm.current_state = "isolated"
        with self.assertRaises(ValueError):
            fsm.process_event("coin")            

    def test_is_accept_state(self):
        """Test checking if current state is an accept state."""

        self.assertTrue(self.fsm.is_accept_state())
        self.fsm.process_event("coin")
        self.assertFalse(self.fsm.is_accept_state())


class TestModuloThreeFSM(unittest.TestCase):
    def test_valid_inputs(self):
        """Test multiple valid inputs."""

        self.assertEqual(mod_three("1101"), 1)
        self.assertEqual(mod_three("1110"), 2)
        self.assertEqual(mod_three("1111"), 0)
        self.assertEqual(mod_three("00000001101"), 1)
        self.assertEqual(mod_three("0"), 0)
        self.assertEqual(mod_three("1"), 1)

    def test_invalid_inputs(self):
        """Test multiple invalid inputs."""

        invalid_inputs = ["", None, "loremipsum"]
        for input_str in invalid_inputs:
            with self.assertRaises(ValueError):
                mod_three(input_str)

if __name__ == "__main__":
    unittest.main()