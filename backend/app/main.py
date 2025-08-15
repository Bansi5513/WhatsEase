# backend/app/main.py
import os
from fastapi import FastAPI, WebSocket, Query, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .routers import users, messages
from .ws_manager import ConnectionManager
from .auth import decode_token
from .bot import bot_response
from .database import messages_col
from datetime import datetime
from bson import ObjectId

load_dotenv()
app = FastAPI()
manager = ConnectionManager()

FRONTEND = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(messages.router)

@app.websocket("/ws/{user_email}")
async def websocket_endpoint(websocket: WebSocket, user_email: str, token: str = Query(None)):
    # validate token
    if not token:
        await websocket.close(code=4001)
        return
    try:
        payload = decode_token(token)
        if payload.get("sub") != user_email:
            await websocket.close(code=4002)
            return
    except Exception:
        await websocket.close(code=4003)
        return

    await manager.connect(user_email, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # expected: {"type":"message", "payload": {sender, recipient, content}}
            if data.get("type") == "message":
                p = data["payload"]
                # store into DB
                doc = {
                    "message_id": str(ObjectId()),
                    "sender": p["sender"],
                    "recipient": p["recipient"],
                    "content": p["content"],
                    "timestamp": datetime.utcnow(),
                    "status": "Sent",
                    "is_bot_response": p.get("is_bot_response", False),
                }
                await messages_col.insert_one(doc)
                # if recipient connected: deliver
                await manager.send_personal(p["recipient"], {"type":"new_message", "message": doc})
                # if recipient is the bot, generate reply and insert/send it
                if p["recipient"] == os.getenv("BOT_EMAIL", "bot@whatsease"):
                    reply_text = bot_response(p["sender"], p["content"])
                    reply_doc = {
                        "message_id": str(ObjectId()),
                        "sender": os.getenv("BOT_EMAIL", "bot@whatsease"),
                        "recipient": p["sender"],
                        "content": reply_text,
                        "timestamp": datetime.utcnow(),
                        "status": "Sent",
                        "is_bot_response": True,
                    }
                    await messages_col.insert_one(reply_doc)
                    # send reply back to the user
                    await manager.send_personal(p["sender"], {"type":"new_message", "message": reply_doc})
    finally:
        manager.disconnect(user_email)
