from abc import ABC, abstractmethod
from utils.get_page_text import get_page_text
from base.schemas import MessagePayload, Vote, VoteInitialisation
import google.auth.transport.requests
import google.oauth2.id_token
import validators
import requests
import os
import logging

class CheckerAgentBase(ABC):
    @abstractmethod
    def check_message(self, message: MessagePayload) -> Vote:
        ## must return an instance of Vote
        pass

    def get_website_content(self, url):
        if validators.url(url):
            return get_page_text(url)
        else:
            raise ValueError(f"Invalid URL: {url}")

    def message_handler(self, message: MessagePayload) -> Vote:
        messageId = message.messageId
        try:
            vote = self.check_message(message)
        except Exception as e:
            raise ValueError(f"Error in check_message implementation: {e}")
        # check if valid Vote 
        if not isinstance(vote, Vote):
            raise TypeError(f"Expected Vote, got {type(vote)} from check_message implementation")
        

        
        api_host = os.getenv("API_HOST")
        agent_name = os.getenv("AGENT_NAME")
        if not api_host:
            raise ValueError("API_HOST environment variable not set")
        if not agent_name:
            raise ValueError("AGENT_NAME environment variable not set")
        
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, api_host)
        headers = {"Authorization": f"Bearer {id_token}"}
        try:
            vote_initialisation = VoteInitialisation(factCheckerName=agent_name)
            res = requests.post(f"{api_host}/messages/{messageId}/voteRequests", json=vote_initialisation.model_dump(mode="json"), headers=headers)
            res.raise_for_status()
            # get response body
            response_body = res.json()
            vote_request_path = response_body.get("voteRequestPath")
        except Exception as e:
            raise ValueError(f"Error creating vote request: {e}")
        
        if not vote_request_path:
            raise ValueError(f"Vote request path not returned as as part of response")
        
        if messageId not in vote_request_path:
            raise ValueError(f"Vote request path does not contain messageId")

        try:
            res = requests.post(f"{api_host}/{vote_request_path}", json=vote.model_dump(mode="json"), headers=headers)
            res.raise_for_status()
        except Exception as e:
            raise ValueError(f"Error updating the vote request: {e}")
            
        logging.info(f"Vote for message {messageId} successfully updated")


