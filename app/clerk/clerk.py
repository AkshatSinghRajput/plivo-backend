from clerk_backend_api import Clerk
from config.config import Config
from utils.logger import logger
import time


# Function to check if a user is part of an organization
async def check_user_in_organization(user_id: str, organization_id: str):
    try:
        # Initialize Clerk API client with bearer authentication
        clerk = Clerk(bearer_auth=Config.CLERK_SECRET_KEY)

        # Fetch user details asynchronously
        user = await clerk.users.get_async(user_id=user_id)
        if not user:
            return {"message": "User not found", "success": False}

        # Fetch organization memberships asynchronously
        organization = await clerk.organization_memberships.list_async(
            organization_id=organization_id
        )

        if not organization:
            logger.error("Organization not found")
            return {"message": "Organization not found", "success": False}

        # Extract member IDs from organization data
        members_id = [member.public_user_data.user_id for member in organization.data]

        # Check if user is part of the organization
        if user_id not in members_id:
            logger.error("User not in organization")
            return {"message": "User not in organization", "success": False}

        return {"message": "User in organization", "success": True}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"message": "An error occurred", "success": False}


# Function to check if a user session is valid and belongs to an organization
async def check_user_session(session_id: str, organization_id: str):
    try:
        # Initialize Clerk API client with bearer authentication
        clerk = Clerk(bearer_auth=Config.CLERK_SECRET_KEY)

        # Fetch session details asynchronously
        user = await clerk.sessions.get_async(session_id=session_id)

        if not user:
            logger.error("User not found")
            return {"message": "User not found", "success": False}

        # Check if user is part of the organization
        organization = await check_user_in_organization(
            user_id=user.user_id, organization_id=organization_id
        )

        # Check if the session is active and the user has the organization_id in the session
        if user.expire_at < int(time.time()) or organization["success"] == False:
            logger.error("Session expired or user not in organization")
            return {"message": "Access denied to secure endpoint", "success": False}

        return {"message": "Access granted to secure endpoint", "success": True}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"message": "An error occurred", "success": False}


# Function to get organization data based on organization slug
async def get_organization_data(organization_slug):
    try:
        # Initialize Clerk API client with bearer authentication
        clerk = Clerk(bearer_auth=Config.CLERK_SECRET_KEY)

        # Fetch organization details asynchronously
        organization = await clerk.organizations.get_async(
            organization_id=organization_slug
        )

        if not organization:
            logger.error("Organization not found")
            return {"message": "Organization not found", "success": False}

        return {
            "data": {
                "organization_id": organization.id,
                "organization_name": organization.name,
            },
            "success": True,
        }
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"message": "An error occurred", "success": False}
