from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from utils.logger import logger
from models.incident import (
    create_incident,
    IncidentModel,
    get_all_incidents,
    get_incident_by_id,
    update_incident,
    delete_incident,
)

router = APIRouter()  # Create a new APIRouter instance


@router.get("/")
async def root():
    return {"message": "Welcome to Incidents API"}  # Root endpoint


@router.get("/get-all-incidents/{organizationId}")
async def get_all_incidents_route(organizationId: str):
    try:
        if not organizationId:  # Check if organizationId is provided
            return JSONResponse(
                {"message": "Missing organization ID", "success": False},
                status_code=401,
            )
        incidents = await get_all_incidents(organizationId)  # Fetch all incidents
        if not incidents:  # Check if incidents are found
            return JSONResponse(
                {"message": "No incidents found", "success": False}, status_code=404
            )

        return JSONResponse(
            {"message": "Incidents found", "success": True, "data": incidents["data"]}
        )
    except Exception as e:
        logger.error(f"Error fetching incidents: {str(e)}")  # Log the error
        return JSONResponse(
            {"message": "Error fetching incidents", "success": False}, status_code=500
        )


@router.get("/get-incident/{organizationId}/{incidentId}")
async def get_incident_route(organizationId: str, incidentId: str):
    try:
        if not incidentId:  # Check if incidentId is provided
            return JSONResponse(
                {"message": "Missing incident ID", "success": False},
                status_code=401,
            )
        incident = await get_incident_by_id(
            incident_id=incidentId, organization_id=organizationId
        )  # Fetch incident by ID

        if not incident:  # Check if incident is found
            return JSONResponse(
                {"message": "Incident not found", "success": False}, status_code=404
            )
        return JSONResponse(
            {"message": "Incident found", "success": True, "data": incident["data"]}
        )
    except Exception as e:
        logger.error(f"Error fetching incident: {str(e)}")  # Log the error
        return JSONResponse(
            {"message": "Error fetching incident", "success": False}, status_code=500
        )


@router.post("/create-incident")
async def create_incident_route(
    incident: IncidentModel,
    organizationId: str = Header(...),
    sessionId: str = Header(...),
):
    try:
        if not incident:  # Check if incident data is provided
            return JSONResponse(
                {"message": "Missing incident data", "success": False},
                status_code=400,
            )
        incident = await create_incident(incident)  # Create a new incident
        if not incident:  # Check if incident creation was successful
            return JSONResponse(
                {"message": "Incident creation failed", "success": False},
                status_code=400,
            )
        return JSONResponse(
            {
                "message": "Incident created successfully",
                "success": True,
            }
        )
    except Exception as e:
        logger.error(f"Error creating incident: {str(e)}")  # Log the error
        return JSONResponse(
            {"message": "Error creating incident", "success": False}, status_code=500
        )


@router.post("/update-incident")
async def update_incident_route(
    incident: IncidentModel,
    organizationId: str = Header(...),
    sessionId: str = Header(...),
):
    try:
        if not incident:  # Check if incident data is provided
            return JSONResponse(
                {"message": "Missing incident data", "success": False},
                status_code=400,
            )
        incident = await update_incident(
            incident=incident, organization_id=organizationId
        )  # Update the incident
        if not incident:  # Check if incident update was successful
            return JSONResponse(
                {"message": "Incident update failed", "success": False},
                status_code=400,
            )
        return JSONResponse(
            {
                "message": "Incident updated successfully",
                "success": True,
            }
        )
    except Exception as e:
        logger.error(f"Error updating incident: {str(e)}")  # Log the error
        return JSONResponse(
            {"message": "Error updating incident", "success": False}, status_code=500
        )


@router.delete("/delete-incident/{incidentId}")
async def delete_incident_route(incidentId: str, organizationId: str = Header(...)):
    try:
        if not incidentId:  # Check if incidentId is provided
            return JSONResponse(
                {"message": "Missing incident ID", "success": False},
                status_code=400,
            )
        incident = await delete_incident(
            incident_id=incidentId, organization_id=organizationId
        )  # Delete the incident
        if not incident:  # Check if incident deletion was successful
            return JSONResponse(
                {"message": "Incident deletion failed", "success": False},
                status_code=400,
            )
        return JSONResponse(
            {
                "message": "Incident deleted successfully",
                "success": True,
            }
        )
    except Exception as e:
        logger.error(f"Error deleting incident: {str(e)}")  # Log the error
        return JSONResponse(
            {"message": "Error deleting incident", "success": False}, status_code=500
        )
