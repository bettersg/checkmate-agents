from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Annotated

class MessageType(Enum):
    TEXT = 'text',
    IMAGE = 'image',

class FactCheckCategory(Enum):
    SCAM= "scam",
    ILLICIT= "illicit",
    IRRELEVANT= "irrelevant"
    SPAM= "spam"
    INFO= "info"
    LEGITIMATE= "legitimate"
    UNSURE= "unsure"

class MessagePayload(BaseModel):
    messageId: str
    type: MessageType
    text: Optional[str] = None
    caption: Optional[str] = None
    storageUrl: Optional[str] = None

class VoteInitialisation(BaseModel):
    factCheckerName: str

class Vote(BaseModel):
    category: FactCheckCategory
    truthScore: Optional[Annotated[int, Field(ge=0, le=5)]] = None