from base.agent_base_class import CheckerAgentBase
import logging
from base.schemas import Vote, MessagePayload, UnsupportedMessageTypeException, MessageType
from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper
import json
from openai import OpenAI
import os
from time import sleep

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

    def search_google(q):
        return json.dumps(tool.run(q))
    
    def agent_report(self, reasoning, category, truth_score = None, subjects = None):
        self.reasoning = reasoning
        self.category = category
        self.truth_score = truth_score
        return "Report Received"

    def check_message(self, message: MessagePayload):
        logging.info(f"Checking message: {message}")

        if message.type != MessageType.TEXT:
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
        
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": message.text,
                }
            ]
        )
        
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_8qTNpp9tqQjkjnj4HhuWDCqs",
        )

        agent_complete = False

        while not agent_complete:
            sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run.status in ["expired", "completed", "failed", "cancelled"]:
                agent_complete = True
            elif run.status == "requires_action":
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                for tool_call in tool_calls:
                    output = process_call(tool_call)
                    run = client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=[
                                {
                                    "tool_call_id": tool_call.id,
                                    "output": output,
                                }
                            ]
                        )
        if not self.category:
            raise ValueError("Category not set")
        elif self.category == "info" and not self.truth_score:
            raise ValueError("Truth score not set for info")
        else:
            logging.info(f"Reported category: {self.category}")
            logging.info(f"Reported truth score: {self.truth_score}")
            logging.info(f"Reported reasoning: {self.reasoning}")

        return Vote(category=self.category, truthScore=int(self.truth_score)) #change this