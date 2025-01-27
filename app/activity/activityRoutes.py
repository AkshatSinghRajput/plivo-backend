from fastapi import APIRouter
from models.activity import (
    create_activity,  # Import function to create an activity
    ActivityModel,  # Import the activity model
    get_all_activities,  # Import function to get all activities
    get_activity_by_actor_id,  # Import function to get activity by actor ID
)
from fastapi import Header
from utils.logger import logger  # Import logger utility
from fastapi.responses import JSONResponse  # Import JSON response utility

router = APIRouter()  # Create a new APIRouter instance


@router.get("/")
async def root():
    # Root endpoint to welcome users
    return {"message": "Welcome to Activity API"}


@router.get("/get-all-activities/{organization_id}")
async def get_all_activities_route(organization_id: str):
    try:
        if not organization_id:
            # Return error if organization ID is missing
            return JSONResponse(
                {"message": "Missing organization ID", "success": False},
                status_code=401,
            )
        activities = await get_all_activities(organization_id)  # Fetch all activities
        if not activities:
            # Return error if no activities found
            return JSONResponse(
                {"message": "No activities found", "success": False}, status_code=404
            )

        # Return success response with activities data
        return JSONResponse(
            {"message": "Activities found", "success": True, "data": activities["data"]}
        )
    except Exception as e:
        logger.error(f"Error fetching activities: {str(e)}")  # Log the error
        # Return error response
        return JSONResponse(
            {"message": "Error fetching activities", "success": False}, status_code=500
        )


@router.get("/get-activity/{organization_id}/{actor_id}")
async def get_activity(organization_id: str, actor_id: str):
    try:
        if not actor_id:
            # Return error if actor ID is missing
            return JSONResponse(
                {"message": "Missing actor ID", "success": False},
                status_code=401,
            )
        if not organization_id:
            # Return error if organization ID is missing
            return JSONResponse(
                {"message": "Missing organization ID", "success": False},
                status_code=401,
            )
        # Fetch activity by actor ID and organization ID
        return await get_activity_by_actor_id(actor_id, organization_id)
    except Exception as e:
        logger.error(f"Error fetching activity: {str(e)}")  # Log the error
        # Return error response
        return JSONResponse(
            {"message": "Error fetching activity", "success": False}, status_code=500
        )


@router.post("/create-activity")
async def create_activity_route(
    activity: ActivityModel,  # Activity data from request body
    organizationId: str = Header(...),  # Organization ID from request header
    sessionId: str = Header(...),  # Session ID from request header
):
    try:
        if not activity:
            # Return error if activity data is missing
            return JSONResponse(
                {"message": "Missing activity data", "success": False}, status_code=401
            )
        activity_created = await create_activity(activity)  # Create new activity
        if activity_created["success"]:
            # Return success response if activity created successfully
            return JSONResponse(
                {"message": "Activity created successfully", "success": True}
            )
        # Return error response if activity creation failed
        return JSONResponse(
            {"message": "Error creating activity", "success": False}, status_code=500
        )
    except Exception as e:
        logger.error(f"Error creating activity: {str(e)}")  # Log the error
        # Return error response
        return JSONResponse(
            {"message": "Error creating activity", "success": False}, status_code=500
        )
