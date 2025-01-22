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

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to Incidents API"}


@router.get("/get-all-incidents/{organizationId}")
async def get_all_incidents_route(organizationId: str):
    try:
        if not organizationId:
            return JSONResponse(
                {"message": "Missing organization ID", "success": False},
                status_code=401,
            )
        incidents = await get_all_incidents(organizationId)
        if not incidents:
            return JSONResponse(
                {"message": "No incidents found", "success": False}, status_code=404
            )

        return JSONResponse(
            {"message": "Incidents found", "success": True, "data": incidents["data"]}
        )
    except Exception as e:
        logger.error(f"Error fetching incidents: {str(e)}")
        return JSONResponse(
            {"message": "Error fetching incidents", "success": False}, status_code=500
        )


@router.get("/get-incident/{organizationId}/{incidentId}")
async def get_incident_route(organizationId: str, incidentId: str):
    try:
        if not incidentId:
            return JSONResponse(
                {"message": "Missing incident ID", "success": False},
                status_code=401,
            )
        incident = await get_incident_by_id(
            incident_id=incidentId, organization_id=organizationId
        )

        if not incident:
            return JSONResponse(
                {"message": "Incident not found", "success": False}, status_code=404
            )
        return JSONResponse(
            {"message": "Incident found", "success": True, "data": incident["data"]}
        )
    except Exception as e:
        logger.error(f"Error fetching incident: {str(e)}")
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
        if not incident:
            return JSONResponse(
                {"message": "Missing incident data", "success": False},
                status_code=400,
            )
        incident = await create_incident(incident)
        if not incident:
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
        logger.error(f"Error creating incident: {str(e)}")
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
        if not incident:
            return JSONResponse(
                {"message": "Missing incident data", "success": False},
                status_code=400,
            )
        incident = await update_incident(
            incident=incident, organization_id=organizationId
        )
        if not incident:
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
        logger.error(f"Error updating incident: {str(e)}")
        return JSONResponse(
            {"message": "Error updating incident", "success": False}, status_code=500
        )


@router.delete("/delete-incident/{incidentId}")
async def delete_incident_route(incidentId: str, organizationId: str = Header(...)):
    try:
        if not incidentId:
            return JSONResponse(
                {"message": "Missing incident ID", "success": False},
                status_code=400,
            )
        incident = await delete_incident(
            incident_id=incidentId, organization_id=organizationId
        )
        if not incident:
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
        logger.error(f"Error deleting incident: {str(e)}")
        return JSONResponse(
            {"message": "Error deleting incident", "success": False}, status_code=500
        )
