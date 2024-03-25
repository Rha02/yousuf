from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.handlers.router import create_router
from app.driver.driver import MongoDB
from dotenv import load_dotenv
import os

load_dotenv()

# Get environment variables
mongodb_uri = os.getenv("MONGODB_URI")
if (mongodb_uri is None):
    print("MONGODB_URI not found in environment variables")
    exit(1)

dbconn = MongoDB(os.getenv("MONGODB_URI"))

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

    router = create_router(dbconn.db)
    
    app.include_router(router) 

    return app

app = create_app()

def start():
    """Start server with 'poetry run start' command"""
    print("SERVER STARTED")
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
