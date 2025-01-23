from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from utils.database import connect_to_mongodb
from utils.logger import logger


# Define the schema for the Service model using Pydantic
class ServiceSchema(BaseModel):
    service_id: str = Field(..., unique=True)  # Unique service ID
    organization_id: str  # ID of the organization
    service_name: str = Field(..., min_length=5, max_length=255)  # Name of the service
    service_description: str = Field(
        ..., min_length=10, max_length=255
    )  # Description of the service
    service_status: Optional[str] = (
        "Operational"  # Status of the service, default is "Operational"
    )
    start_date: Optional[datetime] = Field(
        default_factory=datetime.now().isoformat
    )  # Start date, default is current time


# Connect to MongoDB and get the services collection
db = connect_to_mongodb().Plivo
services_collection = db.services


# Function to create a new service
async def create_service(service: ServiceSchema):
    try:
        # Insert the service into the collection
        created_service = services_collection.insert_one(
            ServiceSchema(**service.dict()).dict()
        )
        if created_service:
            return {"success": True, "message": "Service created successfully"}
        logger.error("Service creation failed")
        return {"success": False, "message": "Service creation failed"}
    except Exception as e:
        logger.error(f"An error occurred in creating Service: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Function to get all services for a specific organization
async def get_all_services(organization_id: str):
    try:
        # Find all services for the given organization ID
        services = services_collection.find(
            {"organization_id": organization_id},
            {
                "_id": 0,
            },
        )
        if services:
            # Convert start_date to ISO format
            services = [
                {**service, "start_date": service["start_date"].isoformat()}
                for service in list(services)
            ]
            return {
                "success": True,
                "message": "Services fetched successfully",
                "data": services,
            }
        logger.error("Services fetch failed")
        return {"success": False, "message": "Services fetch failed"}
    except Exception as e:
        logger.error(f"An error occurred in fetching Services: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Function to get a service by its ID
async def get_service_by_id(service_id: str, organization_id: str):
    try:
        # Find the service with the given service ID
        service = services_collection.find_one(
            {"service_id": service_id, "organization_id": organization_id},
            {
                "_id": 0,
            },
        )
        # Change the date format to ISO format
        if service:
            service["start_date"] = service["start_date"].isoformat()
            return {
                "success": True,
                "message": "Service fetched successfully",
                "data": service,
            }
        logger.error("Service fetch failed")
        return {"success": False, "message": "Service fetch failed"}
    except Exception as e:
        logger.error(f"An error occurred in fetching Service: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Function to update a service
async def update_service(service: ServiceSchema, organization_id: str):
    try:
        # Update the service with the given service ID and organization ID
        updated_service = services_collection.update_one(
            {"service_id": service.service_id, "organization_id": organization_id},
            {"$set": ServiceSchema(**service.dict()).dict()},
        )
        if updated_service:
            return {"success": True, "message": "Service updated successfully"}
        logger.error("Service update failed")
        return {"success": False, "message": "Service update failed"}
    except Exception as e:
        logger.error(f"An error occurred in updating Service: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}


# Function to delete a service
async def delete_service(service_id: str, organization_id: str):
    try:
        # Delete the service with the given service ID and organization ID
        deleted_service = services_collection.delete_one(
            {"service_id": service_id, "organization_id": organization_id}
        )
        if deleted_service:
            return {"success": True, "message": "Service deleted successfully"}
        logger.error("Service deletion failed")
        return {"success": False, "message": "Service deletion failed"}
    except Exception as e:
        logger.error(f"An error occurred in deleting Service: {str(e)}")
        return {"success": False, "message": f"An error occurred: {str(e)}"}
