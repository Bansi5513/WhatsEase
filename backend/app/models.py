# backend/app/models.py
from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime
from typing import Optional

class MessageStatus(str, Enum):
    Sent = "Sent"
    Delivered = "Delivered"
    Read = "Read"

class MessageIn(BaseModel):
    sender: EmailStr
    recipient: EmailStr
    content: str
    is_bot_response: bool = False

class MessageDB(MessageIn):
    message_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: MessageStatus = MessageStatus.Sent

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
