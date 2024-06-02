from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.handlers.router import create_router
from driver.driver import MongoDB
from dotenv import load_dotenv
import os
from app.repository.mongodb_repo import MongoDBRepository
from app.services.auth_repo.jwt_repo import JWTRepository
from app.services.hash_repo.bcrypt_repo import BcryptHashRepository
from app.services.llm_repo.gpt_repo import GPTRepository
from app.config import AppConfig

load_dotenv()

# Get environment variables
mongodb_uri = os.getenv("MONGODB_URI")
if (mongodb_uri is None):
    print("MONGODB_URI not found in environment variables")
    exit(1)

dbname = os.getenv("DB_NAME")

dbconn = MongoDB(mongodb_uri, dbname)

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

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if (openai_api_key is None):
        print("OPENAI_API_KEY not found in environment variables")
        exit(1)

    # Create an authentication token repository
    authrepo = JWTRepository(jwt_secret, jwt_algorithm)

    # Create a hash function repository
    hashrepo = BcryptHashRepository()

    llmrepo = GPTRepository(openai_api_key)

    # Encapsulate services in an AppConfig object
    appConfig = AppConfig(dbrepo, authrepo, hashrepo, llmrepo)

    # Create router and attach router to the app
    router = create_router(appConfig)
    app.include_router(router) 

    return app

app = create_app()

def start():
    """Start server with 'poetry run start' command"""
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
