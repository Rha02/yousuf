import json
from typing import Annotated
from fastapi import APIRouter, File, Form, Response, UploadFile, Request
from app.config import AppConfig
from app.models.user import User
from app.models.chat import Chat

max_messages_limit = 50

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
            "id": user.id,
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
            new_user = app.db.create_user(new_user)
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
            "id": new_user.id,
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
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content=json.dumps({
                    "error": "Invalid authorization header"
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        auth_token = auth_header.split(" ")[1]
        
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return Response(
                content=json.dumps({
                    "error": str(e)
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )

        user_email = payload.get("email")

        user = app.db.get_user_by_email(user_email)
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

        return user
    
    @router.post("/upload_text")
    async def upload_file(
        request: Request,
        file: Annotated[UploadFile, File()]
    ):
        """Upload a text file to the server"""
        # get authentication token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content=json.dumps({
                    "error": "Invalid authorization header"
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        auth_token = auth_header.split(" ")[1]

        # get the file name
        file_name = file.filename
        # get the file extension
        file_extension = file_name.split(".")[-1]
        
        return {
            "file_name": file_name,
            "file_extension": file_extension
        }


    @router.get("/chats")
    async def chats(request: Request):
        """Get the list of chats"""
        # get authentication token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content=json.dumps({
                    "error": "Invalid authorization header"
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        auth_token = auth_header.split(" ")[1]
        
        # get the user's id from the token
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return Response(
                content=json.dumps({
                    "error": str(e)
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        user_id = payload.get("id")

        chats = app.db.get_chats(user_id)

        return chats

    @router.post("/chats")
    async def create_chat(request: Request):
        """Create a new chat"""
        # get authentication token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content=json.dumps({
                    "error": "Invalid authorization header"
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        auth_token = auth_header.split(" ")[1]
        
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return Response(
                content=json.dumps({
                    "error": str(e)
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        user_id = payload.get("id")
        # Check if the user exists
        user = app.db.get_user_by_id(user_id)
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
        
        # get the chat title from the request body
        body = await request.form()
        title = body.get("title")
        if not title:
            return {"error": "Title is required"}

        # create the chat
        chat = app.db.create_chat(Chat(
            id="",
            user_id=user_id,
            title=title
        ))

        if not chat:
            return Response(
                content=json.dumps({
                    "error": "Failed to create chat"
                }),
                status_code=500,
                headers={
                    "Content-Type": "application/json"
                }
            )

        return chat
    
    @router.get("/chats/{chat_id}")
    async def get_messages(chat_id: str, request: Request):
        """Get message/conversation history for a chat"""
        # get authentication token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content=json.dumps({
                    "error": "Invalid authorization header"
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        auth_token = auth_header.split(" ")[1]

        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return Response(
                content=json.dumps({
                    "error": str(e)
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        user_id = payload.get("id")

        # Check if chat's user_id matches the user_id
        chat = app.db.get_chat_by_id(chat_id)
        if not chat:
            return Response(
                content=json.dumps({
                    "error": "Chat not found"
                }),
                status_code=404,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        if chat.user_id != user_id:
            return Response(
                content=json.dumps({
                    "error": "Unauthorized"
                }),
                status_code=403,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        # get query parameters
        limit = request.query_params.get("limit", 10)
        try:
            limit = int(limit)
        except ValueError:
            limit = 10

        if limit < 1 or limit > max_messages_limit:
            limit = 10
        
        offset = request.query_params.get("offset", 0)
        try:
            offset = int(offset)
        except ValueError:
            offset = 0

        messages = app.db.get_messages(chat_id, limit, offset)

        return messages

    @router.post("/chats/{chat_id}/message")
    async def message(chat_id: str, request: Request):
        """Send a message to the LLM"""
        # get authentication token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content=json.dumps({
                    "error": "Invalid authorization header"
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        auth_token = auth_header.split(" ")[1]

        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return Response(
                content=json.dumps({
                    "error": str(e)
                }),
                status_code=401,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        user_id = payload.get("id")

        # Check if chat's user_id matches the user_id
        chat = app.db.get_chat_by_id(chat_id)
        if not chat:
            return Response(
                content=json.dumps({
                    "error": "Chat not found"
                }),
                status_code=404,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        if chat.user_id != user_id:
            return Response(
                content=json.dumps({
                    "error": "Unauthorized"
                }),
                status_code=403,
                headers={
                    "Content-Type": "application/json"
                }
            )
        
        # get the message from the request body
        body = await request.form()
        prompt = body.get("prompt")
        if not prompt:
            return Response(
                content=json.dumps({
                    "error": "Prompt is required"
                }),
                status_code=400,
                headers={
                    "Content-Type": "application/json"
                }
            
            )

        # send the message to the LLM
        response = app.llmrepo.messageLLM(chat_id, prompt)

        return {"message": response}

    return router