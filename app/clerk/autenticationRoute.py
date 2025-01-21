from fastapi import APIRouter
from app.clerk.clerk import check_user_session
from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from utils.logger import logger
from pydantic import BaseModel

import json

app_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Session(BaseModel):
    session_id: str


@app_router.post("/secure-endpoint")
async def secure_endpoint(request: Request):
    try:
        data = await request.json()
        session_id = data["sessionId"]
        organization_id = data["organizationId"]
        user = check_user_session(session_id, organization_id)

        return JSONResponse(
            {"message": "Access granted to secure endpoint", "success": True}
        )
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return JSONResponse(
            {"message": "An error occurred", "success": False}, status_code=500
        )
