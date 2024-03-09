from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Annotated

class MessageType(Enum):
    TEXT = 'text'
    IMAGE = 'image'

class FactCheckCategory(Enum):
    SCAM= "scam"
    ILLICIT= "illicit"
    IRRELEVANT= "irrelevant"
    SPAM= "spam"
    INFO= "info"
    SATIRE= "satire"
    LEGITIMATE= "legitimate"
    UNSURE= "unsure"


class MessagePayload(BaseModel):
    messageId: str = Field(..., description="Unique identifier for the message. Can be ignored for the agent's implementation")
    type: MessageType = Field(..., description="Either 'image' or 'text'. Used to distinguish different types of messages in the pipeline")
    text: Optional[str] = Field(None, description="Only exists if the message type is 'text'. Text contents of the whatsapp message sent in")
    caption: Optional[str] = Field(None, description="Only exists if the message type is 'image'. The caption of the image sent in")
    storageUrl: Optional[str] = Field(None, description="Only exists if the message type is 'image'. The GCP Cloud Storage Bucket URI of the image sent in")

class VoteInitialisation(BaseModel):
    factCheckerName: str

class Vote(BaseModel):
    category: FactCheckCategory
    truthScore: Optional[Annotated[int, Field(ge=1, le=5)]] = None

class UnsupportedMessageTypeException(Exception):
    pass