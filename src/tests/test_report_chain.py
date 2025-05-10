import unittest
from src.chains.report_chain import create_report_chain
from src.state.conversation_state import ConversationState

class TestReportChain(unittest.TestCase):
    def test_chain_creation(self):
        chain = create_report_chain()
        self.assertIsNotNone(chain)

    def test_chain_invoke_valid_input(self):
        chain = create_report_chain()
        test_input = {
            "name": "John Doe",
            "age": "30",
            "complaint_duration": "Headache for 2 days",
            "key_findings_vitals": "BP: 150/95, HR: 80",
            "relevant_history": "Allergic to penicillin"
        }
        response = chain.invoke(test_input)
        self.assertIsInstance(response, str)
        self.assertIn("Patient Summary", response)

    def test_chain_invoke_missing_input(self):
        chain = create_report_chain()
        test_input = {
            "complaint_duration": "Headache for 2 days"
        }
        response = chain.invoke(test_input)
        self.assertIsInstance(response, str)

    def test_conversation_state(self):
        state = ConversationState()
        state.set("test_key", "test_value")
        self.assertEqual(state.get("test_key"), "test_value")
        self.assertEqual(state.get("non_existent", "default"), "default")

if __name__ == "__main__":
    unittest.main()