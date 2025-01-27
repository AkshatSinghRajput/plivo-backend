from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List


class ConnectionManager:
    """Manages WebSocket connections grouped by organization."""

    def __init__(self):
        # Dictionary to store active WebSocket connections grouped by organization ID
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, organization_id: str):
        """Accept a WebSocket connection and group it by organization."""
        await websocket.accept()  # Accept the WebSocket connection
        if organization_id not in self.active_connections:
            # Initialize the list for the organization if it doesn't exist
            self.active_connections[organization_id] = []
        # Add the WebSocket connection to the organization's list
        self.active_connections[organization_id].append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection from the organization."""
        for organization_id, connections in self.active_connections.items():
            if websocket in connections:
                # Remove the WebSocket connection from the organization's list
                connections.remove(websocket)
                if len(connections) == 0:
                    # Remove the organization entry if no connections are left
                    self.active_connections.pop(organization_id)
                break

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        await websocket.send_text(
            message
        )  # Send a text message to the WebSocket connection

    async def broadcast(self, message: str, organization_id: str):
        """Broadcast a message to all active WebSocket connections in the organization."""
        if organization_id in self.active_connections:
            # Iterate through all connections in the organization and send the message
            for connection in self.active_connections[organization_id]:
                await connection.send_text(message)


# Instantiate the ConnectionManager
manager = ConnectionManager()
