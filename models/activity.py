from pydantic import BaseModel, Field
from datetime import datetime
from datetime import timezone
from typing import Optional
from utils.logger import logger
from utils.database import connect_to_mongodb
from app.sockets.sockets import manager


# Define the ActivityModel using Pydantic for data validation
class ActivityModel(BaseModel):
    activity_id: str = Field(..., unique=True, min_length=1)
    organization_id: str = Field(..., min_length=1)
    action: str = Field(..., min_length=1, max_length=255)
    activity_description: str = Field(..., min_length=1, max_length=255)
    actor_id: str = Field(..., min_length=1)
    actor_type: str = Field(..., min_length=1, max_length=255)
    timestamp: Optional[datetime] = Field(
        default_factory=(lambda: datetime.now(timezone.utc))
    )


# Connect to the Plivo database
db = connect_to_mongodb().Plivo

# Fetch the activity collection
activity_collection = db.activities


# Function to create an activity
async def create_activity(activity: ActivityModel):
    try:
        # Insert the activity into the collection
        created_activity = activity_collection.insert_one(
            ActivityModel(**activity.model_dump()).model_dump()
        )
        print("Created Activity", created_activity)
        if created_activity:
            # Send the activity to the socket
            await manager.broadcast("update", organization_id=activity.organization_id)
            logger.info("Activity created successfully ")
            return {"success": True, "message": "Activity created successfully"}
        logger.error("Activity creation failed")
        return {"success": False, "message": "Activity creation failed"}
    except Exception as e:
        logger.error(f"An error occurred in creating Activity: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Function to get all activities for a specific organization
async def get_all_activities(organization_id: str):
    try:
        # Find activities by organization_id
        activities = activity_collection.find(
            {"organization_id": organization_id},
            {
                "_id": 0,
            },
        )
        if activities:
            # Convert the cursor to a list of json objects
            activities = [
                {**activity, "timestamp": activity["timestamp"].isoformat()}
                for activity in activities
            ]
            logger.info("Activities fetched successfully")
            return {
                "success": True,
                "message": "Activities fetched successfully",
                "data": activities,
            }

        logger.error("Failed to fetch activities")
        return {"success": True, "message": "Failed to fetch activities", "data": []}
    except Exception as e:
        logger.error(f"An error occurred in fetching activities: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Function to get activities by actor_id and organization_id
async def get_activity_by_actor_id(actor_id: str, organization_id: str):
    try:
        # Find activities by actor_id and organization_id
        cursor = activity_collection.find(
            {"actor_id": actor_id, "organization_id": organization_id},
            {
                "_id": 0,
            },
        )
        # Convert the cursor to a list of json objects
        activities = [
            {**activity, "timestamp": activity["timestamp"].isoformat()}
            for activity in cursor
        ]
        if activities:
            return {
                "success": True,
                "message": "Activity fetched successfully",
                "data": activities,
            }

        logger.error("Failed to fetch activity")
        return {"success": False, "message": "Failed to fetch activity"}
    except Exception as e:
        logger.error(f"An error occurred in fetching activity: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}
