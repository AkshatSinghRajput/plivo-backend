from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.database import connect_to_mongodb
from utils.logger import logger
from app.clerk.autenticationRoute import app_router

# Create an instance of the FastAPI class
app = FastAPI()

# List of allowed origins for CORS
origins = [
    "http://localhost:3000",
    "http://localhost",
    "https://plivo-phi.vercel.app",
    "https://plivo-phi.vercel.app/",
]

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
    logger.info("Welcome to the AI Objective Suggestion API")
    return {"message": "Welcome to the AI Objective Suggestion API"}


# Include the authentication routes
app.include_router(app_router, prefix="/api/v1/auth")


# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
