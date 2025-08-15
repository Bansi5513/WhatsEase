# backend/app/routers/messages.py
from fastapi import APIRouter, Depends
from ..models import MessageIn, MessageDB, MessageStatus
from ..database import messages_col
from ..auth import get_current_user
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/send")
async def send_message(msg: MessageIn, current_user = Depends(get_current_user)):
    doc = msg.dict()
    doc["message_id"] = str(ObjectId())
    doc["timestamp"] = datetime.utcnow()
    doc["status"] = MessageStatus.Sent.value
    await messages_col.insert_one(doc)
    # return inserted doc (simplified)
    return {"message_id": doc["message_id"]}
