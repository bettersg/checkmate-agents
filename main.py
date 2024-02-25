from dotenv import load_dotenv

load_dotenv()

from cloudevents.http import CloudEvent
import functions_framework
import base64
import json
from base.schemas import MessagePayload
from implementation.agent import CheckerAgent

@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    try:
        # Decode the base64 data
        message_data = base64.b64decode(cloud_event.data["message"]["data"]).decode('utf-8')
        # Convert the decoded data to JSON
        payload = json.loads(message_data)
        validated_payload = MessagePayload(**payload)
        print(f"Validated Payload: {validated_payload}")
    except Exception as e:
        raise ValueError(f"Invalid or malformed data: {e}")
    
    CheckerAgent.message_handler(validated_payload)
    
    

    
    
    


