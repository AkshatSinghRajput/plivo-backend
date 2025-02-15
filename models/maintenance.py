from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from utils.database import connect_to_mongodb
from utils.logger import logger
from models.activity import create_activity, ActivityModel
import uuid


# Define the Maintenance model using Pydantic
class Maintenance(BaseModel):
    maintenance_id: str = Field(..., unique=True)
    service_impacted: List[str] = Field(...)
    organization_id: str = Field(...)
    maintenance_name: str = Field(...)
    maintenance_description: str = Field(...)
    maintenance_status: str = Field(default="Scheduled")
    start_from: datetime = Field(...)
    end_at: datetime = Field(...)


# Connect to MongoDB and get the maintenances collection
db = connect_to_mongodb().Plivo
maintenance_collection = db.maintenances


# Retrieve all maintenance records for a given organization
async def get_all_maintenances(organization_id: str):
    try:
        # Query maintenances collection excluding MongoDB _id field
        maintenances = maintenance_collection.find(
            {"organization_id": organization_id},
            {
                "_id": 0,
            },
        )
        if maintenances:
            # Convert datetime objects to ISO format strings
            maintenances = [
                {
                    **maintenance,
                    "start_from": maintenance["start_from"].isoformat(),
                    "end_at": maintenance["end_at"].isoformat(),
                }
                for maintenance in list(maintenances)
            ]
            return {
                "success": True,
                "data": maintenances,
                "message": "Maintenances retrieved successfully",
            }
        logger.error("No maintenances found")
        return {"success": False, "message": "No maintenances found"}

    except Exception as e:
        logger.error(f"An error occurred in getting maintenances: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Retrieve a specific maintenance record by ID and organization
async def get_maintenance_by_id(maintenance_id: str, organization_id: str):
    try:
        # Query for specific maintenance record
        maintenance = maintenance_collection.find_one(
            {"maintenance_id": maintenance_id, "organization_id": organization_id},
            {
                "_id": 0,
            },
        )
        if maintenance:
            # Convert datetime objects to ISO format
            maintenance["start_from"] = maintenance["start_from"].isoformat()
            maintenance["end_at"] = maintenance["end_at"].isoformat()
            return {
                "success": True,
                "data": maintenance,
                "message": "Maintenance retrieved successfully",
            }
        logger.error("No maintenance found")
        return {"success": False, "message": "No maintenance found"}

    except Exception as e:
        logger.error(f"An error occurred in getting maintenance: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Create a new maintenance record and associated activity
async def create_maintenance(maintenance: Maintenance):
    try:
        # Insert new maintenance record
        created_maintenance = maintenance_collection.insert_one(
            Maintenance(**maintenance.model_dump()).model_dump()
        )
        if not created_maintenance:
            logger.error("Maintenance creation failed")
            return {"success": False, "message": "Maintenance creation failed"}

        # Create an activity log for the new maintenance
        activity = await create_activity(
            ActivityModel(
                activity_id=str(uuid.uuid4()),
                organization_id=maintenance.organization_id,
                actor_type="maintenance",
                activity_description=f"New maintenance {maintenance.maintenance_name} created",
                actor_id=maintenance.maintenance_id,
                action=maintenance.maintenance_status,
            )
        )

        if activity["success"]:
            return {
                "success": True,
                "message": "Maintenance created successfully",
            }
        else:
            logger.error("Activity creation failed")
            return {"success": False, "message": "Activity creation failed"}

    except Exception as e:
        logger.error(f"An error occurred in creating maintenance: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Update an existing maintenance record and log status changes
async def update_maintenance(maintenance: Maintenance, organization_id: str):
    try:
        # Verify maintenance exists
        current_maintenance = await get_maintenance_by_id(
            maintenance.maintenance_id, organization_id
        )
        if not current_maintenance["success"]:
            return current_maintenance

        current_maintenance = current_maintenance["data"]

        # Create activity log if maintenance status has changed
        if current_maintenance["maintenance_status"] != maintenance.maintenance_status:
            activity = await create_activity(
                ActivityModel(
                    activity_id=str(uuid.uuid4()),
                    actor_id=maintenance.maintenance_id,
                    actor_type="maintenance",
                    organization_id=organization_id,
                    action=maintenance.maintenance_status,
                    activity_description=f"Maintenance {maintenance.maintenance_name} updated with status {maintenance.maintenance_status}",
                )
            )

            if not activity["success"]:
                logger.error("Activity creation failed")
                return {"success": False, "message": "Activity creation failed"}

        # Update maintenance record
        updated_maintenance = maintenance_collection.update_one(
            {"maintenance_id": maintenance.maintenance_id},
            {"$set": Maintenance(**maintenance.dict()).dict()},
        )
        if updated_maintenance:
            return {
                "success": True,
                "message": "Maintenance updated successfully",
            }
        logger.error("Maintenance update failed")
        return {"success": False, "message": "Maintenance update failed"}

    except Exception as e:
        logger.error(f"An error occurred in updating maintenance: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Delete a maintenance record for a given organization
async def delete_maintenance(maintenance_id: str, organization_id: str):
    try:
        # Remove maintenance record
        deleted_maintenance = maintenance_collection.delete_one(
            {"maintenance_id": maintenance_id, "organization_id": organization_id}
        )
        if deleted_maintenance:
            return {
                "success": True,
                "message": "Maintenance deleted successfully",
            }
        logger.error("Maintenance deletion failed")
        return {"success": False, "message": "Maintenance deletion failed"}

    except Exception as e:
        logger.error(f"An error occurred in deleting maintenance: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}
