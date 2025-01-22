from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from utils.logger import logger
from models.publicPage import get_public_page_data

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to Public Page API"}


@router.get("/get-public-page-data/{organization_id}")
async def get_public_page_data_route(organization_id: str):
    try:
        incidents = await get_public_page_data(organization_id)
        if not incidents["success"]:
            return JSONResponse(
                {"message": "Incidents fetch failed", "success": False}, status_code=404
            )

        return JSONResponse(
            {
                "message": "Incidents fetched successfully",
                "data": incidents["data"],
                "success": True,
            }
        )
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"message": "An error occurred", "success": False}
