import json
from typing import Annotated
from fastapi import APIRouter, File, Form, Response, UploadFile, Request
from app.config import AppConfig

def create_router(app: AppConfig):
    """Create an instance of the FastAPI application"""
    router = APIRouter()

    @router.post("/login")
    async def login(email: str = Form(), password: str = Form()):
        auth_token = app.authrepo.create_token({
            "email": email
        })

        body = {
            "message": "Login Successful"
        }

        res = Response(
            content=json.dumps(body),
            status_code=200,
            headers={
                "Authorization": "Bearer " + auth_token,
                "Content-Type": "application/json"
            }
        )
        return res

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
    async def user(request: Request):
        auth_header = request.headers.get("Authorization")
        auth_token = auth_header.split(" ")[1]
        if not auth_token:
            return {"error": "Authentication token is required"}
        
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return {"error": str(e)}

        return payload
    
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