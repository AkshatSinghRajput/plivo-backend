# Import required libraries and modules
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from utils.database import connect_to_mongodb
from utils.logger import logger
from models.activity import create_activity, ActivityModel
import uuid
from typing import Optional


# Define Incident data model using Pydantic
class IncidentModel(BaseModel):
    incident_id: str = Field(..., unique=True)  # Unique identifier for each incident
    service_impacted: List[str] = Field(...)  # List of services affected by incident
    organization_id: str = Field(...)  # Organization identifier
    incident_name: str = Field(
        ..., min_length=5, max_length=255
    )  # Name with length constraints
    incident_description: str = Field(
        ..., min_length=5, max_length=255
    )  # Description with length constraints
    incident_status: str = Field(default="Operational")  # Current status of incident
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now().isoformat()
    )  # Timestamp of creation


# Initialize database connection
db = connect_to_mongodb().Plivo
incident_collection = db.incidents


async def get_all_incidents(organization_id: str):
    """Retrieve all incidents for a given organization"""
    try:
        # Query database excluding MongoDB's _id field
        incidents = incident_collection.find(
            {"organization_id": organization_id},
            {
                "_id": 0,
            },
        )
        if incidents:
            # Convert datetime to ISO format for JSON serialization
            incidents = [
                {**incident, "created_at": incident["created_at"].isoformat()}
                for incident in list(incidents)
            ]
            return {
                "success": True,
                "data": incidents,
                "message": "Incidents retrieved successfully",
            }
        logger.error("No incidents found")
        return {"success": False, "message": "No incidents found"}

    except Exception as e:
        logger.error(f"An error occurred in getting incidents: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


async def get_incident_by_id(incident_id: str, organization_id: str):
    """Retrieve a specific incident by ID"""
    try:
        # Find incident matching both incident_id and organization_id
        incident = incident_collection.find_one(
            {"incident_id": incident_id, "organization_id": organization_id},
            {
                "_id": 0,
            },
        )
        if incident:
            incident["created_at"] = incident["created_at"].isoformat()
            return {
                "success": True,
                "data": incident,
                "message": "Incident retrieved successfully",
            }
        logger.error("Incident not found")
        return {"success": False, "message": "Incident not found"}
    except Exception as e:
        logger.error(f"An error occurred in getting incident: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


async def create_incident(incident: IncidentModel):
    """Create a new incident and log the activity"""
    try:
        # Insert new incident into database
        created_incident = incident_collection.insert_one(
            IncidentModel(**incident.dict()).dict()
        )
        if not created_incident:
            logger.error("Incident creation failed")
            return {"success": False, "message": "Incident creation failed"}

        # Create an activity log for the new incident
        activity = await create_activity(
            ActivityModel(
                activity_id=str(uuid.uuid4()),
                actor_id=incident.incident_id,
                actor_type="incident",
                organization_id=incident.organization_id,
                action=incident.incident_status,
                activity_description=f"Incident {incident.incident_name} created with status {incident.incident_status}",
            )
        )

        if activity["success"]:
            return {"success": True, "message": "Incident created successfully"}

        logger.error("Incident creation failed")
        return {"success": False, "message": "Incident creation failed"}
    except Exception as e:
        logger.error(f"An error occurred in creating Incident: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


async def update_incident(incident: IncidentModel, organization_id: str):
    """Update an existing incident and log status changes"""
    try:
        # Check if incident exists
        current_incident = await get_incident_by_id(
            incident.incident_id, organization_id
        )
        if not current_incident["success"]:
            return {"success": False, "message": "Incident not found"}
        current_incident = current_incident["data"]

        # Log activity if incident status has changed
        if current_incident["incident_status"] != incident.incident_status:
            activity = await create_activity(
                ActivityModel(
                    activity_id=str(uuid.uuid4()),
                    actor_id=incident.incident_id,
                    actor_type="incident",
                    organization_id=organization_id,
                    action=incident.incident_status,
                    activity_description=f"Incident {incident.incident_name} updated with status {incident.incident_status}",
                )
            )

            if not activity["success"]:
                return {"success": False, "message": "Incident update failed"}

        # Update incident in database
        updated_incident = incident_collection.update_one(
            {"incident_id": incident.incident_id, "organization_id": organization_id},
            {"$set": IncidentModel(**incident.dict()).dict()},
        )
        if updated_incident:
            return {"success": True, "message": "Incident updated successfully"}
        logger.error("Incident update failed")
        return {"success": False, "message": "Incident update failed"}
    except Exception as e:
        logger.error(f"An error occurred in updating Incident: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


async def delete_incident(incident_id: str, organization_id: str):
    """Delete an incident from the database"""
    try:
        # Remove incident matching both incident_id and organization_id
        deleted_incident = incident_collection.delete_one(
            {"incident_id": incident_id, "organization_id": organization_id}
        )
        if deleted_incident:
            return {"success": True, "message": "Incident deleted successfully"}
        logger.error("Incident deletion failed")
        return {"success": False, "message": "Incident deletion failed"}
    except Exception as e:
        logger.error(f"An error occurred in deleting Incident: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}
