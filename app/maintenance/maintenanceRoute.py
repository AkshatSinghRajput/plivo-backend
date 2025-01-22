from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from utils.logger import logger
from models.maintenance import (
    create_maintenance,
    Maintenance,
    get_all_maintenances,
    get_maintenance_by_id,
    update_maintenance,
    delete_maintenance,
)

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to Maintenance API"}


@router.get("/get-all-maintenances/{organizationId}")
async def get_all_maintenances_route(organizationId: str):
    try:
        if not organizationId:
            return JSONResponse(
                {"message": "Missing organization ID", "success": False},
                status_code=401,
            )
        maintenances = await get_all_maintenances(organizationId)
        if not maintenances:
            return JSONResponse(
                {"message": "No maintenances found", "success": False}, status_code=404
            )

        return JSONResponse(
            {
                "message": "Maintenances found",
                "success": True,
                "data": maintenances["data"],
            }
        )
    except Exception as e:
        logger.error(f"Error fetching maintenances: {str(e)}")
        return JSONResponse(
            {"message": "Error fetching maintenances", "success": False},
            status_code=500,
        )


@router.get("/get-maintenance/{organizationId}/{maintenanceId}")
async def get_maintenance_route(organizationId: str, maintenanceId: str):
    try:
        if not maintenanceId:
            return JSONResponse(
                {"message": "Missing maintenance ID", "success": False},
                status_code=401,
            )
        maintenance = await get_maintenance_by_id(
            maintenance_id=maintenanceId, organization_id=organizationId
        )

        if not maintenance:
            return JSONResponse(
                {"message": "Maintenance not found", "success": False}, status_code=404
            )
        return JSONResponse(
            {
                "message": "Maintenance found",
                "success": True,
                "data": maintenance["data"],
            }
        )
    except Exception as e:
        logger.error(f"Error fetching maintenance: {str(e)}")
        return JSONResponse(
            {"message": "Error fetching maintenance", "success": False}, status_code=500
        )


@router.post("/create-maintenance")
async def create_maintenance_route(
    maintenance: Maintenance,
    organizationId: str = Header(...),
    sessionId: str = Header(...),
):
    try:
        if not maintenance:
            return JSONResponse(
                {"message": "Missing maintenance data", "success": False},
                status_code=401,
            )
        maintenance = await create_maintenance(maintenance)

        if not maintenance:
            return JSONResponse(
                {"message": "Error creating maintenance", "success": False},
                status_code=400,
            )

        return JSONResponse(
            {
                "message": "Maintenance created",
                "success": True,
            },
            status_code=200,
        )
    except Exception as e:
        logger.error(f"Error creating maintenance: {str(e)}")
        return JSONResponse(
            {"message": "Error creating maintenance", "success": False},
            status_code=500,
        )


@router.post("/update-maintenance")
async def update_maintenance_route(
    maintenance: Maintenance,
    organizationId: str = Header(...),
    sessionId: str = Header(...),
):
    try:
        if not maintenance:
            return JSONResponse(
                {"message": "Missing maintenance data", "success": False},
                status_code=401,
            )
        maintenance = await update_maintenance(
            maintenance=maintenance, organization_id=organizationId
        )

        if not maintenance:
            return JSONResponse(
                {"message": "Error updating maintenance", "success": False},
                status_code=400,
            )

        return JSONResponse(
            {
                "message": "Maintenance updated",
                "success": True,
            },
            status_code=200,
        )
    except Exception as e:
        logger.error(f"Error updating maintenance: {str(e)}")
        return JSONResponse(
            {"message": "Error updating maintenance", "success": False},
            status_code=500,
        )


@router.delete("/delete-maintenance/{maintenanceId}")
async def delete_maintenance_route(
    maintenanceId: str, organizationId: str = Header(...)
):
    try:
        if not maintenanceId:
            return JSONResponse(
                {"message": "Missing maintenance ID", "success": False},
                status_code=401,
            )
        maintenance = await delete_maintenance(
            maintenance_id=maintenanceId, organization_id=organizationId
        )

        if not maintenance:
            return JSONResponse(
                {"message": "Error deleting maintenance", "success": False},
                status_code=400,
            )

        return JSONResponse(
            {
                "message": "Maintenance deleted",
                "success": True,
            },
            status_code=200,
        )
    except Exception as e:
        logger.error(f"Error deleting maintenance: {str(e)}")
        return JSONResponse(
            {"message": "Error deleting maintenance", "success": False},
            status_code=500,
        )
