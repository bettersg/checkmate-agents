from base.agent_base_class import CheckerAgentBase
import logging
from base.schemas import Vote

class CheckerAgent(CheckerAgentBase):
    def check_message(self, message):
        logging.info(f"Checking message: {message}")

        ##TODO: Implement your message checking logic here
        
        return Vote(category="unsure", truthScore=None) #change this. You must return an instance of class Vote.