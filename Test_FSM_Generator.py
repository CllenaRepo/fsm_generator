import unittest
from FSM_generator import FiniteStateMachine

class TestFiniteStateMachine(unittest.TestCase):
    def setUp(self):
        """Set up a new FSM instance for each test."""
        self.fsm = FiniteStateMachine()
        self.fsm.add_state("locked", is_accept=True)
        self.fsm.add_state("unlocked")
        self.fsm.add_transition("locked", "coin", "unlocked")
        self.fsm.add_transition("unlocked", "push", "locked")
        self.fsm.add_transition("locked", "push", "locked")
        self.fsm.add_transition("unlocked", "coin", "unlocked")

    def test_add_state(self):
        """Test adding states and setting initial state."""
        fsm = FiniteStateMachine()
        fsm.add_state("test_state")
        self.assertIn("test_state", fsm.states)
        self.assertEqual(fsm.initial_state, "test_state")
        self.assertEqual(fsm.current_state, "test_state")

    def test_add_accept_state(self):
        """Test adding an accept state."""
        fsm = FiniteStateMachine()
        fsm.add_state("accept_state", is_accept=True)
        self.assertIn("accept_state", fsm.accept_states)
        self.assertTrue(fsm.is_accept_state())

    def test_add_transition(self):
        """Test adding a valid transition."""
        self.assertIn("locked", self.fsm.transitions)
        self.assertEqual(self.fsm.transitions["locked"]["coin"], "unlocked")

    def test_add_invalid_transition(self):
        """Test adding a transition with non-existent states."""
        with self.assertRaises(ValueError):
            self.fsm.add_transition("nonexistent", "event", "locked")
        with self.assertRaises(ValueError):
            self.fsm.add_transition("locked", "event", "nonexistent")

    def test_process_event_valid(self):
        """Test processing valid events."""
        self.assertEqual(self.fsm.get_current_state(), "locked")
        self.fsm.process_event("coin")
        self.assertEqual(self.fsm.get_current_state(), "unlocked")
        self.fsm.process_event("push")
        self.assertEqual(self.fsm.get_current_state(), "locked")

    def test_process_event_invalid_state(self):
        """Test processing an event from a state with no transitions."""
        fsm = FiniteStateMachine()
        fsm.add_state("isolated")
        fsm.current_state = "isolated"
        with self.assertRaises(ValueError):
            fsm.process_event("coin")

    def test_process_event_invalid_event(self):
        """Test processing an undefined event."""
        with self.assertRaises(ValueError):
            self.fsm.process_event("invalid_event")

    def test_is_accept_state(self):
        """Test checking if current state is an accept state."""
        self.assertTrue(self.fsm.is_accept_state())
        self.fsm.process_event("coin")
        self.assertFalse(self.fsm.is_accept_state())

    def test_reset(self):
        """Test resetting to initial state."""
        self.fsm.process_event("coin")
        self.assertEqual(self.fsm.get_current_state(), "unlocked")
        self.fsm.reset()
        self.assertEqual(self.fsm.get_current_state(), "locked")

    def test_multiple_transitions(self):
        """Test multiple transitions in sequence."""
        self.fsm.process_event("coin")
        self.fsm.process_event("coin")
        self.assertEqual(self.fsm.get_current_state(), "unlocked")
        self.fsm.process_event("push")
        self.assertEqual(self.fsm.get_current_state(), "locked")
        self.fsm.process_event("push")
        self.assertEqual(self.fsm.get_current_state(), "locked")

if __name__ == "__main__":
    unittest.main()