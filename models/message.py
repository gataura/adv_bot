from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class File(BaseModel):
    key: str
    name: str
    file_type: str
    size: int
    width: Optional[int] = None
    height: Optional[int] = None

class Button(BaseModel):
    text: str
    url: Optional[str] = None
    data: Optional[str] = None

class EntityType(str, Enum):
    DISCUSSION = "discussion",
    THREAD = "thread",
    USER = "user"

class Message(BaseModel):
    entity_type: EntityType = EntityType.DISCUSSION  # По умолчанию "discussion"
    entity_id: int
    content: str
    files: Optional[List[File]] = None
    buttons: Optional[List[List[Button]]] = None
    parent_message_id: Optional[int] = None
    display_avatar_url: Optional[str] = None
    display_name: Optional[str] = None
    skip_invite_mentions: bool = False
    link_preview: bool = False

    def dict(self, **kwargs):
        # Переопределяем метод dict для кастомной сериализации
        data = super().dict(**kwargs)
        # Преобразуем Enum в его значение
        if 'entity_type' in data:
            data['entity_type'] = data['entity_type'].value
        return data

class MessageWrapper(BaseModel):
    message: Message