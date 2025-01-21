from fastapi import APIRouter
from models.activity import create_activity, ActivityModel, get_all_activities

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Welcome to Activity API"}


@router.get("/get-all-activities/{organization_id}")
async def get_all_activities_route(organization_id: str):
    activities = await get_all_activities(organization_id)
    return activities


@router.post("/create-activity")
async def create_activity_route(activity: ActivityModel):
    return await create_activity(activity)
