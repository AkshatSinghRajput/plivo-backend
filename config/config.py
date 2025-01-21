import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY")
    CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
    CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SIGNING_SECRET = os.getenv("SIGNING_SECRET")
