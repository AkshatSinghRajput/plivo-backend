from fastapi import APIRouter
from models.activity import (
    create_activity,
    ActivityModel,
    get_all_activities,
    get_activity_by_actor_id,
)
from fastapi import Header
from utils.logger import logger
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to Activity API"}


@router.get("/get-all-activities/{organization_id}")
async def get_all_activities_route(organization_id: str):
    try:
        if not organization_id:
            return JSONResponse(
                {"message": "Missing organization ID", "success": False},
                status_code=401,
            )
        activities = await get_all_activities(organization_id)
        if not activities:
            return JSONResponse(
                {"message": "No activities found", "success": False}, status_code=404
            )

        return JSONResponse(
            {"message": "Activities found", "success": True, "data": activities["data"]}
        )
    except Exception as e:
        logger.error(f"Error fetching activities: {str(e)}")
        return JSONResponse(
            {"message": "Error fetching activities", "success": False}, status_code=500
        )


@router.get("/get-activity/{organization_id}/{actor_id}")
async def get_activity(organization_id: str, actor_id: str):
    try:
        if not actor_id:
            return JSONResponse(
                {"message": "Missing actor ID", "success": False},
                status_code=401,
            )
        if not organization_id:
            return JSONResponse(
                {"message": "Missing organization ID", "success": False},
                status_code=401,
            )
        return await get_activity_by_actor_id(actor_id, organization_id)
    except Exception as e:
        logger.error(f"Error fetching activity: {str(e)}")
        return JSONResponse(
            {"message": "Error fetching activity", "success": False}, status_code=500
        )


@router.post("/create-activity")
async def create_activity_route(
    activity: ActivityModel,
    organizationId: str = Header(...),
    sessionId: str = Header(...),
):
    try:

        if not activity:
            return JSONResponse(
                {"message": "Missing activity data", "success": False}, status_code=401
            )
        activity_created = await create_activity(activity)
        if activity_created["success"]:
            return JSONResponse(
                {"message": "Activity created successfully", "success": True}
            )
        return JSONResponse(
            {"message": "Error creating activity", "success": False}, status_code=500
        )
    except Exception as e:
        logger.error(f"Error creating activity: {str(e)}")
        return JSONResponse(
            {"message": "Error creating activity", "success": False}, status_code=500
        )
