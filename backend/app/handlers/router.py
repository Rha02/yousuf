import datetime
import os
from typing import Annotated
from app.models.uploaded_file import UploadedFile
from fastapi import APIRouter, File, Form, UploadFile, Request
from app.config import AppConfig
from app.models.user import User
from app.models.chat import Chat
from app.utils import http as httpUtils
from langchain_community.document_loaders import TextLoader
import re

max_messages_limit = 50

def create_router(app: AppConfig):
    """Create an instance of the FastAPI application"""
    router = APIRouter()

    @router.post("/login")
    async def login(email: str = Form(), password: str = Form()):
        # Email length: 1 to 256 characters
        # Format: local@domain.com
        # Local: Letters, digits, and special characters from ._%+-
        # Local Length (before @): 3 to 64 characters
        # Domain: Letters, digits, dots, and hyphens
        # Domain Length (after @): 1 to 255 characters
        # No consecutive dots and no whitespaces
        # End matches top-level domain starting with . and at least two characters
        emailPattern = r'^(?=.{1,256}$)(?=.{3,64}@.{1,255}$)(?!.*\s)(?!.*\.{2})[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(emailPattern, email):
            return httpUtils.jsonResponse({
                "error": "Invalid email"
            }, 400)
             
        user = app.db.get_user_by_email(email)
        if not user:
            return httpUtils.ErrorResponses.USER_NOT_FOUND
        
        if not app.hashrepo.compare(password, user.password):
            return httpUtils.ErrorResponses.INCORRECT_PASSWORD

        auth_token = app.authrepo.create_token({
            "id": user.id,
            "email": email
        })

        body = {
            "message": "Login Successful"
        }

        res = httpUtils.jsonResponse(body, 200)
        res.headers["Authorization"] = "Bearer " + auth_token

        return res

    @router.post("/register")
    async def register(
        first_name: str = Form(), 
        last_name: str = Form(), 
        email: str = Form(),
        password: str = Form()
    ):
        # Regex explanation in login()
        emailPattern = r'^(?=.{1,256}$)(?=.{3,64}@.{1,255}$)(?!.*\s)(?!.*\.{2})[a-zA-Z0-9._%+-]{1,64}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.fullmatch(emailPattern, email):
            return httpUtils.jsonResponse({
                "error": "Invalid email"
            }, 400)
            
        # At least one character, one digit, and one special character from !@#$%^&*()_+=[\]{};":\\|,.<>?
        # At least 8 characters long
        # Cannot contain whitespaces
        passwordPattern =  r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+=[\]{};":\\|,.<>?])(?=\S)(?=.{8,}).*$'
        if not re.fullmatch(passwordPattern, password):
            return httpUtils.jsonResponse({
                "error": "Invalid password"
            }, 400)
            
        # First Name & Last Name
        # Letters only
        # Name length: 2 to 50 characters
        namePattern = r'^[a-zA-Z]{2,50}$'
        if not re.fullmatch(namePattern, first_name):
            return httpUtils.jsonResponse({
                "error": "Invalid first name"
            }, 400)
        if not re.fullmatch(namePattern, last_name):
            return httpUtils.jsonResponse({
                "error": "Invalid last name"
            }, 400)
        
        try:
            hashed_password = app.hashrepo.hash(password)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 500)
        
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
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 500)
    
        auth_token = app.authrepo.create_token({
            "id": new_user.id,
            "email": email
        })

        res = httpUtils.jsonResponse({
            "message": "User registered successfully"
        }, 201)
        res.headers["Authorization"] = "Bearer " + auth_token
        return res

    @router.post("/logout")
    async def logout():
        return {"message": "Logout"}

    @router.get("/user")
    async def user(request: Request):
        auth_token = httpUtils.getAuthToken(request)
        if not auth_token:
            return httpUtils.ErrorResponses.INVALID_AUTH_TOKEN
        
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 401)

        user_email = payload.get("email")

        user = app.db.get_user_by_email(user_email)
        if not user:
            return httpUtils.ErrorResponses.USER_NOT_FOUND

        return user

    @router.get("/chats")
    async def chats(request: Request):
        """Get the list of chats"""
        # get authentication token
        auth_token = httpUtils.getAuthToken(request)
        if not auth_token:
            return httpUtils.ErrorResponses.INVALID_AUTH_TOKEN
        
        # get the user's id from the token
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 401)
        
        user_id = payload.get("id")

        chats = app.db.get_chats(user_id)

        return chats

    @router.post("/chats")
    async def create_chat(request: Request):
        """Create a new chat"""
        # get authentication token
        auth_token = httpUtils.getAuthToken(request)
        if not auth_token:
            return httpUtils.ErrorResponses.INVALID_AUTH_TOKEN
        
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 401)
        
        user_id = payload.get("id")
        # Check if the user exists
        user = app.db.get_user_by_id(user_id)
        if not user:
            return httpUtils.ErrorResponses.USER_NOT_FOUND
        
        # get the chat title from the request body
        body = await request.form()
        title = body.get("title")
        if not title:
            return httpUtils.jsonResponse({
                "error": "Title is required"
            }, 400)

        # create the chat
        chat = app.db.create_chat(Chat(
            id="",
            user_id=user_id,
            title=title
        ))

        if not chat:
            return httpUtils.jsonResponse({
                "error": "Failed to create chat"
            }, 500)

        return chat
    
    @router.post("/chats/create")
    async def create_chat(request: Request):
        """Create a new chat with first message"""
        # get authentication token
        auth_token = httpUtils.getAuthToken(request)
        if not auth_token:
            return httpUtils.ErrorResponses.INVALID_AUTH_TOKEN
        
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 401)
        
        user_id = payload.get("id")
        # Check if the user exists
        user = app.db.get_user_by_id(user_id)
        if not user:
            return httpUtils.ErrorResponses.USER_NOT_FOUND
        
        # get the message from the request body
        body = await request.form()
        prompt = body.get("prompt")
        if not prompt:
            return httpUtils.jsonResponse({
                "error": "Prompt is required"
            }, 400)
        
        # Create LLM query to create chat title
        query = "Create a short chat title based on the following prompt:\n" + prompt
        title = app.llmrepo.simple_query(query)

        # create the chat
        chat = app.db.create_chat(Chat(
            id="",
            user_id=user_id,
            title=title
        ))

        if not chat:
            return httpUtils.jsonResponse({
                "error": "Failed to create chat"
            }, 500)
        
        # send message to LLM
        response = app.llmrepo.messageLLM(chat.id, prompt)

        return {
            "chat": chat,
            "message": response
        }
    
    @router.get("/chats/{chat_id}")
    async def get_messages(chat_id: str, request: Request):
        """Get message/conversation history for a chat"""
        # get authentication token
        auth_token = httpUtils.getAuthToken(request)
        if not auth_token:
            return httpUtils.ErrorResponses.INVALID_AUTH_TOKEN

        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 401)
        
        user_id = payload.get("id")

        # Check if chat's user_id matches the user_id
        chat = app.db.get_chat_by_id(chat_id)
        if not chat:
            return httpUtils.ErrorResponses.CHAT_NOT_FOUND
        
        if chat.user_id != user_id:
            return httpUtils.ErrorResponses.FORBIDDEN
        
        # get query parameters
        limit = httpUtils.getIntQueryParam(request, "limit", 10)
        if limit < 1 or limit > max_messages_limit:
            limit = 10
        
        offset = httpUtils.getIntQueryParam(request, "offset", 0)

        messages = app.db.get_messages(chat_id, limit, offset)

        return messages

    @router.post("/chats/{chat_id}/message")
    async def message(chat_id: str, request: Request):
        """Send a message to the LLM"""
        # get authentication token
        auth_token = httpUtils.getAuthToken(request)
        if not auth_token:
            return httpUtils.ErrorResponses.INVALID_AUTH_TOKEN

        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 401)
        
        user_id = payload.get("id")

        # Check if chat's user_id matches the user_id
        chat = app.db.get_chat_by_id(chat_id)
        if not chat:
            return httpUtils.ErrorResponses.CHAT_NOT_FOUND
        
        if chat.user_id != user_id:
            return httpUtils.ErrorResponses.FORBIDDEN
        
        # get the message from the request body
        body = await request.form()
        prompt = body.get("prompt")
        if not prompt:
            return httpUtils.jsonResponse({
                "error": "Prompt is required"
            }, 400)

        # send the message to the LLM
        response = app.llmrepo.messageLLM(chat_id, prompt)

        return {"message": response}
    
    @router.post("/chats/{chat_id}/upload_text")
    async def upload_file(
        chat_id: str,
        request: Request,
        file: Annotated[UploadFile, File()]
    ):
        """Upload a text file to the server"""
        # get authentication token
        auth_token = httpUtils.getAuthToken(request)
        if not auth_token:
            return httpUtils.ErrorResponses.INVALID_AUTH_TOKEN
        
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 401)
        
        user_id = payload.get("id")

        # Check if chat's user_id matches the user_id
        chat = app.db.get_chat_by_id(chat_id)
        if not chat:
            return httpUtils.ErrorResponses.CHAT_NOT_FOUND
        
        if chat.user_id != user_id:
            return httpUtils.ErrorResponses.FORBIDDEN

        # get the file name
        file_name = file.filename

        # get the file extension
        file_extension = file_name.split(".")[-1]

        save_dir = "temp/"

        os.makedirs(save_dir, exist_ok=True)

        with open(save_dir + file_name, "wb") as f:
            f.write(file.file.read())

        # Add the file metadata to the database
        uploaded_file = app.db.create_file(
            UploadedFile(
                id="",
                chat_id=chat_id,
                file_name=file_name,
                file_size=os.path.getsize(save_dir + file_name),
                file_type=file_extension,
                uploaded_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        loader = TextLoader(save_dir + file_name, encoding="utf-8")
        docs = loader.load()

        app.llmrepo.add_document(docs[0], chat_id)

        # remove the file
        os.remove(save_dir + file_name)
        
        return uploaded_file
    
    @router.get("/chats/{chat_id}/uploaded_texts")
    async def get_texts(chat_id: str, request: Request):
        """Get the list of uploaded texts"""
        # get authentication token
        auth_token = httpUtils.getAuthToken(request)
        if not auth_token:
            return httpUtils.ErrorResponses.INVALID_AUTH_TOKEN
        
        try:
            payload = app.authrepo.parse_token(auth_token)
        except Exception as e:
            return httpUtils.jsonResponse({
                "error": str(e)
            }, 401)
        
        user_id = payload.get("id")

        # Check if chat's user_id matches the user_id
        chat = app.db.get_chat_by_id(chat_id)
        if not chat:
            return httpUtils.ErrorResponses.CHAT_NOT_FOUND
        
        if chat.user_id != user_id:
            return httpUtils.ErrorResponses.FORBIDDEN

        docs = app.db.get_files(chat_id)

        return docs

    return router