from pydantic import BaseModel, Field
from models.activity import ActivityModel, get_activity_by_actor_id
from utils.database import connect_to_mongodb
from utils.logger import logger
from models.incident import get_all_incidents
from models.maintenance import get_all_maintenances
from datetime import datetime
import asyncio
import json


class publicPageData(BaseModel):
    incident_id: str = Field(..., unique=True)  # Unique service ID
    organization_id: str  # ID of the organization
    incident_name: str = Field(..., min_length=5, max_length=255)  # Name of the service
    incident_description: str = Field(
        ..., min_length=10, max_length=255
    )  # Description of the service
    incident_type: str
    activities: list[ActivityModel]
    service_impacted: list[str]
    created_at: datetime


# Connect to MongoDB and get collections
db = connect_to_mongodb().Plivo
incidents_collection = db.incidents
activity_collection = db.activities
maintenance_collection = db.maintenance


async def get_incidents_with_activities(organization_id: str):
    try:
        # Fetch all incidents for the organization
        incidents = await get_all_incidents(organization_id)
        if not incidents["success"]:
            return {"success": False, "message": "Incidents fetch failed"}

        incidents_data = incidents["data"]

        async def fetch_activities(incident):
            # Fetch activities for a specific incident
            activities = await get_activity_by_actor_id(
                incident["incident_id"], organization_id=organization_id
            )
            if not activities["success"]:
                return None
            return {
                "incident_id": incident["incident_id"],
                "activities": activities["data"],
            }

        # Fetch all activities concurrently
        activities_tasks = [fetch_activities(incident) for incident in incidents_data]
        activities_results = await asyncio.gather(*activities_tasks)

        # Update incidents with their activities
        for result in activities_results:
            if result is None:
                return {"success": False, "message": "Activities fetch failed"}
            for incident in incidents_data:
                if incident["incident_id"] == result["incident_id"]:
                    incident["activities"] = result["activities"]

        # Convert the date to ISO string in activities
        for incident in incidents_data:
            for activity in incident["activities"]:
                activity["timestamp"] = activity["timestamp"]

        # Convert the output into the desired format
        incidents_data = [
            json.loads(
                publicPageData(
                    incident_id=incident["incident_id"],
                    organization_id=incident["organization_id"],
                    incident_name=incident["incident_name"],
                    incident_description=incident["incident_description"],
                    incident_type="Incident",
                    activities=incident["activities"],
                    service_impacted=incident["service_impacted"],
                    created_at=incident["created_at"],
                ).json()
            )
            for incident in incidents_data
        ]
        return {"success": True, "data": incidents_data}

    except Exception as e:
        logger.error(f"An error occurred in fetching Incidents: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


async def get_maintenance_with_activities(organization_id: str):
    try:
        # Fetch all maintenance records for the organization
        maintenance = await get_all_maintenances(organization_id)
        if not maintenance["success"]:
            return {"success": False, "message": "Maintenance fetch failed"}

        maintenance_data = maintenance["data"]

        async def fetch_activities(maintenance):
            # Fetch activities for a specific maintenance record
            activities = await get_activity_by_actor_id(
                maintenance["maintenance_id"], organization_id=organization_id
            )
            if not activities["success"]:
                return None
            return {
                "maintenance_id": maintenance["maintenance_id"],
                "activities": activities["data"],
            }

        # Fetch all activities concurrently
        activities_tasks = [
            fetch_activities(maintenance) for maintenance in maintenance_data
        ]
        activities_results = await asyncio.gather(*activities_tasks)

        # Update maintenance records with their activities
        for result in activities_results:
            if result is None:
                return {"success": False, "message": "Activities fetch failed"}
            for maintenance in maintenance_data:
                if maintenance["maintenance_id"] == result["maintenance_id"]:
                    maintenance["activities"] = result["activities"]

        # Convert the date to ISO string in activities
        for maintenance in maintenance_data:
            for activity in maintenance["activities"]:
                activity["timestamp"] = activity["timestamp"]

        # Convert the output into the desired format
        maintenance_data = [
            json.loads(
                publicPageData(
                    incident_id=maintenance["maintenance_id"],
                    organization_id=maintenance["organization_id"],
                    incident_name=maintenance["maintenance_name"],
                    incident_description=maintenance["maintenance_description"],
                    incident_type="Maintenance",
                    activities=maintenance["activities"],
                    created_at=maintenance["start_from"],
                    service_impacted=maintenance["service_impacted"],
                ).json()
            )
            for maintenance in maintenance_data
        ]
        return {"success": True, "data": maintenance_data}

    except Exception as e:
        logger.error(f"An error occurred in fetching Maintenance: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


async def get_public_page_data(organization_id: str):
    try:
        # Run both fetches concurrently
        incidents_task = get_incidents_with_activities(organization_id)
        maintenance_task = get_maintenance_with_activities(organization_id)
        incidents_result, maintenance_result = await asyncio.gather(
            incidents_task, maintenance_task
        )

        if not incidents_result["success"]:
            return {"success": False, "message": "Incidents fetch failed"}
        if not maintenance_result["success"]:
            return {"success": False, "message": "Maintenance fetch failed"}

        # Combine the results
        combined_data = incidents_result["data"] + maintenance_result["data"]

        return {"success": True, "data": combined_data}
    except Exception as e:
        logger.error(f"An error occurred in fetching Public Page Data: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}
