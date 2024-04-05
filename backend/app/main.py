from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.handlers.router import create_router
from app.driver.driver import MongoDB
from dotenv import load_dotenv
import os
from app.repository.mongodb_repo import MongoDBRepository
from app.services.auth_repo.jwt_repo import JWTRepository
from app.services.hash_repo.test_repo import TestHashRepository
from app.config import AppConfig

load_dotenv()

# Get environment variables
mongodb_uri = os.getenv("MONGODB_URI")
if (mongodb_uri is None):
    print("MONGODB_URI not found in environment variables")
    exit(1)

dbconn = MongoDB(os.getenv("MONGODB_URI"))

dbrepo = MongoDBRepository(dbconn)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for the lifespan of the FastAPI application"""
    try:
        yield
    finally:
        dbconn.close()
        print("MongoDB connection closed")

def create_app():
    """Create an instance of the FastAPI application"""
    app = FastAPI(lifespan=lifespan)
    print("Connecting to MongoDB...")
    try:
        dbconn.client.admin.command("ping")
        print("Pinged MongoDB successfully")
    except Exception as e:
        print("Failed to connect to MongoDB")
        print(e)
        exit(1)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Create app configuration
    jwt_secret = os.getenv("JWT_SECRET")
    if (jwt_secret is None):
        print("JWT_SECRET not found in environment variables")
        exit(1)

    jwt_algorithm = os.getenv("JWT_ALGORITHM")
    if (jwt_algorithm is None):
        print("JWT_ALGORITHM not found in environment variables")
        exit(1)

    # Create an authentication token repository
    authrepo = JWTRepository(jwt_secret, jwt_algorithm)

    # Create a hash function repository
    hashrepo = TestHashRepository()

    # Encapsulate services in an AppConfig object
    appConfig = AppConfig(dbrepo, authrepo, hashrepo)

    # Create router and attach router to the app
    router = create_router(appConfig)
    app.include_router(router) 

    return app

app = create_app()

def start():
    """Start server with 'poetry run start' command"""
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
