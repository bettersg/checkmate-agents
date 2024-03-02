import unittest
from base.schemas import Vote, MessagePayload, UnsupportedMessageTypeException
from implementation.agent import CheckerAgent


class TestCheckerAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CheckerAgent()
        self.text_payload = {
            "messageId": "123",
            "type": "text",
            "text": "BREAKING: Singapore Tourism Board reveals it is paying Taylor Swift $13m to sing Majulah Singapura as a surpise song",
            "caption": None,
            "storageUrl": None,
        }
    
    def test_text_message(self):
        payload = MessagePayload(**self.text_payload)
        vote = self.agent.check_message(payload)
        try:
            vote = self.agent.check_message(payload)
            self.assertIsInstance(vote, Vote)
        except UnsupportedMessageTypeException:
            pass

if __name__ == "__main__":
    unittest.main()