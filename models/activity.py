from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from utils.logger import logger
from utils.database import connect_to_mongodb


class ActivityModel(BaseModel):
    activity_id: str = Field(..., unique=True)
    organization_id: str
    action: str
    activity_description: str
    actor_id: str
    actor_type: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


# Connect to the Pilvo database
db = connect_to_mongodb().Pilvo

# Fetch the activity collection
activity_collection = db.activities


## Function to create an activity
async def create_activity(activity: ActivityModel):
    try:
        created_activity = activity_collection.insert_one({**activity.dict()})
        if created_activity:
            logger.info("Activity created successfully ")
            return {"success": True, "message": "Activity created successfully"}
        logger.error("Activity creation failed")
        return {"success": False, "message": "Activity creation failed"}
    except Exception as e:
        logger.error(f"An error occurred in creating Activity: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


## Function to get all activities
async def get_all_activities(organization_id: str):
    try:
        activities = activity_collection.find({"organization_id": organization_id})
        if activities:
            logger.info("Activities fetched successfully")
            return {
                "success": True,
                "message": "Activities fetched successfully",
                "data": activities,
            }
        logger.error("Failed to fetch activities")
        return {"success": False, "message": "Failed to fetch activities"}
    except Exception as e:
        logger.error(f"An error occurred in fetching activities: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}
