import json
from typing import Annotated
from fastapi import APIRouter, File, Form, Response, UploadFile, Request
from app.config import AppConfig
from app.models.user import User

def create_router(app: AppConfig):
    """Create an instance of the FastAPI application"""
    router = APIRouter()

    @router.post("/login")
    async def login(email: str = Form(), password: str = Form()):
        user = app.db.get_user_by_email(email)
        if not user:
            return Response(
                content=json.dumps({
                    "error": "User not found"
                }),
                status_code=404,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        if not app.hashrepo.compare(password, user.password):
            return Response(
                content=json.dumps({
                    "error": "Incorrect password"
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )

        auth_token = app.authrepo.create_token({
            "email": email
        })

        body = {
            "message": "Login Successful"
        }

        return Response(
            content=json.dumps(body),
            status_code=200,
            headers={
                "Authorization": "Bearer " + auth_token,
                "Content-Type": "application/json"
            }
        )

    @router.post("/register")
    async def register(
        first_name: str = Form(), 
        last_name: str = Form(), 
        email: str = Form(),
        password: str = Form()
    ):
        try:
            hashed_password = app.hashrepo.hash(password)
        except Exception as e:
            return Response(
                content=json.dumps({
                    "error": str(e)
                }),
                status_code=500,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        new_user = User(
            id="",
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )

        try:
            app.db.create_user(new_user)
        except Exception as e:
            return Response(
                content=json.dumps({
                    "error": str(e)
                }),
                status_code=500,
                headers={
                    "Content-Type": "application/json"
                }
            )

        auth_token = app.authrepo.create_token({
            "email": email
        })

        return Response(
            content=json.dumps({
                "message": "User registered successfully"
            }),
            status_code=201,
            headers={
                "Authorization": "Bearer " + auth_token,
                "Content-Type": "application/json"
            }
        )

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

        user_email = payload.get("email")

        user = app.db.get_user_by_email(user_email)

        return user
    
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

    @router.post("/message")
    async def message(request: Request):
        """Send a message to the LLM"""
        # get authentication token
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            return {"error": "Authentication token is required"}
        
        # get the message from the request body
        body = await request.form()

        prompt = body.get("prompt")
        if not prompt:
            return {"error": "Prompt is required"}

        # send the message to the LLM
        response = app.llmrepo.messageLLM("chat_id", prompt)

        return {"message": response}

    return router