from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import connect_to_mongodb
from utils.logger import logger
from app.clerk.clerk import check_user_session, get_organization_data
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.activity.activityRoutes import router as activity_router
from app.services.serviceRoute import router as service_router
from app.incident.incidentRoute import router as incident_router
from app.maintenance.maintenanceRoute import router as maintenance_router
from app.publicPage.publicRoutes import router as public_page_router
import json


# Create an instance of the FastAPI class
app = FastAPI()

# List of allowed origins for CORS
origins = [
    "http://localhost:3000",
    "http://localhost",
    "https://plivo-phi.vercel.app",
    "https://plivo-phi.vercel.app/",
]


@app.middleware("http")
async def session_middleware(request: Request, call_next):
    # Allow GET requests and specific paths without authentication
    if request.method == "GET" or request.url.path[1:] in [
        "docs",
        "openapi.json",
        "favicon.ico",
    ]:
        return await call_next(request)

    try:

        # Retrieve session and organization IDs from headers
        session_id = request.headers.get("sessionId")
        organization_id = request.headers.get("organizationId")

        # Check if session or organization ID is missing
        if not session_id or not organization_id:
            logger.error("Missing session or organization ID")
            return JSONResponse(
                {"message": "Missing session or organization ID", "success": False},
                status_code=401,
            )

        # Check user session validity
        user = await check_user_session(session_id, organization_id)

        # If authentication fails, return 401 response
        if not user["success"]:
            logger.error("Authentication failed")
            return JSONResponse(
                {"message": "Authentication failed", "success": False}, status_code=401
            )

        # Proceed to the next middleware or route handler
        return await call_next(request)

    except Exception as e:
        # Log any exceptions that occur
        logger.error(f"Middleware error: {str(e)}")
        return JSONResponse(
            {"message": "Authentication failed", "success": False}, status_code=401
        )


# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Event handler for the startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Connecting to MongoDB")
    connect_to_mongodb()  # Connect to MongoDB


# Define a root endpoint
@app.get("/")
async def root():
    logger.info("Welcome to the Stato-gram API")
    return {"message": "Welcome to the Stato-gram API"}


@app.get("/api/v1/get-organization-id/{organization_slug}")
async def get_organization_id(organization_slug: str):
    try:
        organization_data = await get_organization_data(organization_slug)

        if not organization_data["success"]:
            return JSONResponse(
                {"message": "Organization not found", "success": False}, status_code=404
            )
        return JSONResponse(
            {
                "message": "Organization found",
                "data": organization_data["data"],
                "success": True,
            }
        )
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"message": "An error occurred", "success": False}


# @app.get("/api/v1/get-incidents-with-activities/{organization_id}")
# async def get_incidents_with_activities_route(organization_id: str):
#     try:
#         incidents = await get_public_page_data(organization_id)
#         if not incidents["success"]:
#             return JSONResponse(
#                 {"message": "Incidents fetch failed", "success": False}, status_code=404
#             )

#         return JSONResponse(
#             {
#                 "message": "Incidents fetched successfully",
#                 "data": incidents["data"],
#                 "success": True,
#             }
#         )
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#         return {"message": "An error occurred", "success": False}


## Import the routers
app.include_router(activity_router, prefix="/api/v1/activity", tags=["Activity"])

app.include_router(service_router, prefix="/api/v1/service", tags=["Service"])

app.include_router(incident_router, prefix="/api/v1/incident", tags=["Incident"])

app.include_router(
    maintenance_router, prefix="/api/v1/maintenance", tags=["Maintenance"]
)

app.include_router(
    public_page_router, prefix="/api/v1/public-page", tags=["Public Page"]
)

# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
