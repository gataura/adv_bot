from pydantic import BaseModel
from typing import Optional
from enum import Enum
from .message import EntityType

class Event(str, Enum):
    NEW = "new",
    UPDATE = "update",
    DELETE = "delete"

class Thread(BaseModel):
    message_id: int
    message_chat_id: int

class IncomingMessage(BaseModel):
    type: str
    id: int
    event: Event
    entity_type: EntityType
    entity_id: int
    content: str
    user_id: int
    created_at: str
    url: str
    chat_id: int
    parent_message_id: Optional[int] = None
    thread: Optional[Thread] = None