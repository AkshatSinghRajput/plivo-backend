from clerk_backend_api import Clerk
from config.config import Config
import time


def check_user_in_organization(user_id: str, organization_id: str):
    try:
        clerk = Clerk(bearer_auth=Config.CLERK_SECRET_KEY)
        user = clerk.users.get(user_id=user_id)
        if not user:
            return {"message": "User not found", "success": False}

        organization = clerk.organization_memberships.list(
            organization_id=organization_id
        )

        if not organization:
            return {"message": "Organization not found", "success": False}

        members_id = [member.public_user_data.user_id for member in organization.data]

        if user_id not in members_id:
            return {"message": "User not in organization", "success": False}

        return {"message": "User in organization", "success": True}
    except Exception as e:
        print("An error occurred: ", str(e))
        return {"message": "An error occurred", "success": False}


def check_user_session(session_id: str, organization_id: str):
    try:

        clerk = Clerk(bearer_auth=Config.CLERK_SECRET_KEY)
        user = clerk.sessions.get(session_id=session_id)
        if not user:
            return {"message": "Access denied to secure endpoint", "success": False}

        ## Check if the session is active and the user has the organization_id in the session
        if (
            user.expire_at < int(time.time())
            or check_user_in_organization(user.user_id, organization_id)["success"]
        ):
            return {"message": "Access denied to secure endpoint", "success": False}

        return {"message": "Access granted to secure endpoint", "success": True}
    except Exception as e:
        print("An error occurred: ", str(e))
        return {"message": "An error occurred", "success": False}
