from typing import Annotated
from fastapi import APIRouter, File, Form, UploadFile, Request
from app.repository.repository import DatabaseRepository

def create_router(db: DatabaseRepository):
    """Create an instance of the FastAPI application"""
    router = APIRouter()

    @router.post("/login")
    async def login(
        email: str = Form(),
        password: str = Form()
    ):
        return {
            "email": email,
            "password": password
        }

    @router.post("/register")
    async def register(
        first_name: str = Form(),
        last_name: str = Form(),
        email: str = Form(),
        password: str = Form()
    ):
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }

    @router.post("/logout")
    async def logout():
        return {"message": "Logout"}

    @router.get("/user")
    async def user():
        return {"message": "User"}
    
    @router.post("/upload_text")
    async def upload_file(
        request: Request,
        file: Annotated[UploadFile, File()]
    ):
        """Upload a text file to the server"""
        # get authentication token
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            return {"error": "Authentication token is required"}

        # get the file name
        file_name = file.filename
        # get the file extension
        file_extension = file_name.split(".")[-1]
        
        return {
            "file_name": file_name,
            "file_extension": file_extension
        }

    return router