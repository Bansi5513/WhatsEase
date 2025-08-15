# backend/app/ws_manager.py
from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.connections.pop(user_id, None)

    async def send_personal(self, user_id: str, message: dict):
        ws = self.connections.get(user_id)
        if ws:
            await ws.send_json(message)

    async def broadcast(self, message: dict):
        for ws in list(self.connections.values()):
            await ws.send_json(message)
