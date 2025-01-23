from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List


class ConnectionManager:
    """Manages WebSocket connections grouped by organization."""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, organization_id: str):
        """Accept a WebSocket connection and group it by organization."""
        await websocket.accept()
        if organization_id not in self.active_connections:
            self.active_connections[organization_id] = []
        self.active_connections[organization_id].append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from the organization."""

        for organization_id, connections in self.active_connections.items():
            if websocket in connections:
                connections.remove(websocket)
                if len(connections) == 0:
                    self.active_connections.pop(organization_id)
                break

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        await websocket.send_text(message)

    async def broadcast(self, message: str, organization_id: str):
        """Broadcast a message to all active WebSocket connections in the organization."""
        if organization_id in self.active_connections:
            for connection in self.active_connections[organization_id]:
                await connection.send_text(message)


# Instantiate the ConnectionManager
manager = ConnectionManager()
