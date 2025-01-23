from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.services import (
    create_service,
    ServiceSchema,
    get_all_services,
    get_service_by_id,
    update_service,
    delete_service,
)
from fastapi import Header
from utils.logger import logger
from models.activity import create_activity, ActivityModel

router = APIRouter()


# Root endpoint
@router.get("/")
async def root():
    return {"message": "Welcome to Services API"}


# Endpoint to get all services for a given organization
@router.get("/get-all-services/{organization_id}")
async def get_all_services_route(organization_id: str):
    try:
        if not organization_id:
            return JSONResponse(
                {"message": "Missing organization ID", "success": False},
                status_code=401,
            )
        services = await get_all_services(organization_id)
        if not services:
            return JSONResponse(
                {"message": "No services found", "success": False}, status_code=404
            )

        return JSONResponse(
            {"message": "Services found", "success": True, "data": services["data"]}
        )
    except Exception as e:
        logger.error(f"Error fetching services: {str(e)}")
        return JSONResponse(
            {"message": "Error fetching services", "success": False}, status_code=500
        )


# Endpoint to get a specific service by its ID and organization ID
@router.get("/get-service/{organization_id}/{service_id}")
async def get_service_route(organization_id: str, service_id: str):
    try:
        if not service_id:
            return JSONResponse(
                {"message": "Missing service ID", "success": False},
                status_code=401,
            )
        service = await get_service_by_id(
            service_id=service_id, organization_id=organization_id
        )
        if not service:
            return JSONResponse(
                {"message": "Service not found", "success": False}, status_code=404
            )

        return JSONResponse(
            {"message": "Service found", "success": True, "data": service["data"]}
        )
    except Exception as e:
        logger.error(f"Error fetching service: {str(e)}")
        return JSONResponse(
            {"message": "Error fetching service", "success": False}, status_code=500
        )


# Endpoint to create a new service
@router.post("/create-service")
async def create_service_route(
    service: ServiceSchema,
    organizationId: str = Header(...),
    sessionId: str = Header(...),
):
    try:
        if not service:
            return JSONResponse(
                {"message": "Missing service data", "success": False},
                status_code=401,
            )
        service_created = await create_service(service)
        if service_created:
            return JSONResponse(
                {"message": "Service created successfully", "success": True}
            )
        logger.error("Service creation failed")
        return JSONResponse(
            {"message": "Service creation failed", "success": False}, status_code=500
        )
    except Exception as e:
        logger.error(f"Error creating service: {str(e)}")
        return JSONResponse(
            {"message": "Error creating service", "success": False}, status_code=500
        )


# Endpoint to update an existing service
@router.post("/update-service")
async def update_service_route(
    service: ServiceSchema,
    organizationId: str = Header(...),
    sessionId: str = Header(...),
):
    try:
        if not service:
            return JSONResponse(
                {"message": "Missing service data", "success": False},
                status_code=401,
            )
        service_updated = await update_service(
            service=service, organization_id=organizationId
        )
        if service_updated:
            return JSONResponse(
                {"message": "Service updated successfully", "success": True}
            )
        logger.error("Service update failed")
        return JSONResponse(
            {"message": "Service update failed", "success": False}, status_code=500
        )
    except Exception as e:
        logger.error(f"Error updating service: {str(e)}")
        return JSONResponse(
            {"message": "Error updating service", "success": False}, status_code=500
        )


# Endpoint to delete a service by its ID
@router.delete("/delete-service/{service_id}")
async def delete_service_route(
    service_id: str, organizationId: str = Header(...), sessionId: str = Header(...)
):
    try:
        if not service_id:
            return JSONResponse(
                {"message": "Missing service ID", "success": False},
                status_code=401,
            )

        service_deleted = await delete_service(
            service_id=service_id, organization_id=organizationId
        )
        if service_deleted:
            return JSONResponse(
                {"message": "Service deleted successfully", "success": True}
            )
        logger.error("Service deletion failed")
        return JSONResponse(
            {"message": "Service deletion failed", "success": False}, status_code=500
        )
    except Exception as e:
        logger.error(f"Error deleting service: {str(e)}")
        return JSONResponse(
            {"message": "Error deleting service", "success": False}, status_code=500
        )
