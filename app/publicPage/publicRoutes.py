from fastapi import APIRouter, Header, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from utils.logger import logger
from models.publicPage import get_public_page_data
from app.sockets.sockets import manager

# Create a new APIRouter instance
router = APIRouter()


# Define a root endpoint that returns a welcome message
@router.get("/")
async def root():
    return {"message": "Welcome to Public Page API"}


# Define an endpoint to get public page data for a specific organization
@router.get("/get-public-page-data/{organization_id}")
async def get_public_page_data_route(organization_id: str):
    try:
        # Fetch incidents data for the given organization_id
        incidents = await get_public_page_data(organization_id)
        if not incidents["success"]:
            # Return a 404 response if fetching incidents failed
            return JSONResponse(
                {"message": "Incidents fetch failed", "success": False}, status_code=404
            )

        # Return the fetched incidents data
        return JSONResponse(
            {
                "message": "Incidents fetched successfully",
                "data": incidents["data"],
                "success": True,
            }
        )
    except Exception as e:
        # Log the error and return a generic error message
        logger.error(f"An error occurred: {str(e)}")
        return {"message": "An error occurred", "success": False}


# Define a WebSocket endpoint for updates
@router.websocket("/update")
async def websocket_endpoint(websocket: WebSocket, organization_id: str = Query(...)):
    # Connect the WebSocket client to the manager
    await manager.connect(websocket, organization_id)
    try:
        while True:
            # Continuously receive data from the WebSocket
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        # Disconnect the WebSocket client if the connection is closed
        manager.disconnect(websocket)
