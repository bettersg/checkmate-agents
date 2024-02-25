from base.agent_base_class import CheckerAgentBase
import logging
from base.schemas import Vote
from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper
import json
from openai import OpenAI
import os

search = GoogleSearchAPIWrapper(google_api_key=os.getenv("GOOGLE_SEARCH_API_KEY"))

client = OpenAI()

def top10(query):
    return search.results(query, 10)

tool = Tool(
    name="Google Search",
    description="Search Google, and get back the top 10 most relevant links to your query, each with a snippet.",
    func=top10,
)


class CheckerAgent(CheckerAgentBase):
    def check_message(self, message):
        logging.info(f"Checking message: {message}")

        ##TODO: Implement your message checking logic here
        
        return Vote(category="unsure", truthScore=None) #change this. You must return an instance of class Vote.
    
    def search_google(self, q):
        return json.dumps(tool.run(q))
    
    def agent_report(self, reasoning, category, truth_score = None, subjects = None) -> Vote:
        return Vote(category=category, truthScore=truth_score)