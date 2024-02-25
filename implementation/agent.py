from base.agent_base_class import CheckerAgentBase
import logging
from base.schemas import Vote, MessagePayload, UnsupportedMessageTypeException
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
    def check_message(self, message: MessagePayload):
        logging.info(f"Checking message: {message}")

        if message.type != "text":
            raise UnsupportedMessageTypeException(f"Invalid message type: {message.type}")

        ##tool caller
        tool_dict = {
            "searchGoogle": self.search_google,
            "getPageText": self.get_website_content,
            "fileReport": self.agent_report,
        }

        def process_call(tool_call):
            id = tool_call.id
            function_name = tool_call.function.name
            function_arguments = json.loads(tool_call.function.arguments)
            output = tool_dict[function_name](**function_arguments)
            return output
        
        # thread = client.beta.threads.create(
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": message.text,
        #         }
        #     ]
        # )
        
        # run = client.beta.threads.runs.create(
        #     thread_id=thread.id,
        #     assistant_id="TO FILL",
        # )

        
        return Vote(category="unsure", truthScore=None) #change this