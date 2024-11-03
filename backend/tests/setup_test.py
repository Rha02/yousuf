from app.repository.test_db import TestDBRepository
from app.services.llm_repo.test_repo import TestLLMRepository
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from app.config import AppConfig
from app.handlers.router import create_router
from app.services.auth_repo.test_repo import TestAuthTokenRepository
from app.services.hash_repo.test_repo import TestHashRepository

def create_test_app():
    """Create an instance of the FastAPI application"""
    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Create an authentication token repository
    authrepo = TestAuthTokenRepository()

    # Create a hash function repository
    hashrepo = TestHashRepository()

    llmrepo = TestLLMRepository()

    dbrepo = TestDBRepository()

    # Encapsulate services in an AppConfig object
    appConfig = AppConfig(dbrepo, authrepo, hashrepo, llmrepo)

    # Create router and attach router to the app
    router = create_router(appConfig)
    app.include_router(router) 

    return app

app = create_test_app()

client = TestClient(app)