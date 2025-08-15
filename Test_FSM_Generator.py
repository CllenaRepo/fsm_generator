import unittest
from FSM_Generator import create_modthree_fsm

class TestFiniteStateMachine(unittest.TestCase):
    def setUp(self):
        """Set up a new FSM instance for each test."""

        self.mod3_fsm = create_modthree_fsm()

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

        mod3_fsm = create_modthree_fsm()
        mod3_fsm.add_state("S3")
        mod3_fsm.add_transition_function("S3", "0", "S0")
        self.assertIn("S3", mod3_fsm.transitions)
        self.assertEqual(mod3_fsm.transitions["S3"]["0"], "S0")

    def test_add_invalid_transition(self):
        """Test adding a transition with non-existent states."""

        with self.assertRaises(ValueError):
            self.mod3_fsm.add_transition_function("loremipsum", "loremipsum", "loremipsum")
        with self.assertRaises(ValueError):
            self.mod3_fsm.add_transition_function("loremipsum", "loremipsum", "loremipsum")

    def test_process_event_valid(self):
        """Test processing valid events."""

        self.assertEqual(self.mod3_fsm.get_current_state(), "S0")
        self.mod3_fsm.process_event("0")
        self.assertEqual(self.mod3_fsm.get_current_state(), "S0")
        self.mod3_fsm.process_event("1")
        self.assertEqual(self.mod3_fsm.get_current_state(), "S1")


        self.mod3_fsm.process_event("0")
        self.assertEqual(self.mod3_fsm.get_current_state(), "S2")
        self.mod3_fsm.current_state = "S1"
        self.mod3_fsm.process_event("1")
        self.assertEqual(self.mod3_fsm.get_current_state(), "S0")

        self.mod3_fsm.current_state = "S2"
        self.mod3_fsm.process_event("0")
        self.assertEqual(self.mod3_fsm.get_current_state(), "S1")
        self.mod3_fsm.current_state = "S2"
        self.mod3_fsm.process_event("1")
        self.assertEqual(self.mod3_fsm.get_current_state(), "S2")

    def test_process_event_invalid_state(self):
        """Test processing an event from a state with no transitions."""

        mod3_fsm = create_modthree_fsm()
        mod3_fsm.add_state("S100")
        mod3_fsm.current_state = "S100"
        with self.assertRaises(ValueError):
            mod3_fsm.process_event("0")

    def test_process_event_invalid_event(self):
        """Test processing an undefined event."""

        with self.assertRaises(ValueError):
            self.mod3_fsm.process_event("invalid_event")

    def test_is_accept_state(self):
        """Test checking if current state is an accept state."""

        self.assertTrue(self.mod3_fsm.is_accept_state())

    def test_multiple_transitions(self):
        """Test multiple transitions in sequence."""

        self.mod3_fsm.process_event("1")
        self.mod3_fsm.process_event("1")
        self.mod3_fsm.process_event("0")
        self.mod3_fsm.process_event("1")
        self.assertEqual(self.mod3_fsm.get_curr_final_state(), 1)

        self.mod3_fsm.current_state = "S0"

        self.mod3_fsm.process_event("1")
        self.mod3_fsm.process_event("1")
        self.mod3_fsm.process_event("1")
        self.mod3_fsm.process_event("0")
        self.assertEqual(self.mod3_fsm.get_curr_final_state(), 2)

        self.mod3_fsm.current_state = "S0"

        self.mod3_fsm.process_event("1")
        self.mod3_fsm.process_event("1")
        self.mod3_fsm.process_event("1")
        self.mod3_fsm.process_event("1")
        self.assertEqual(self.mod3_fsm.get_curr_final_state(), 0)

if __name__ == "__main__":
    unittest.main()