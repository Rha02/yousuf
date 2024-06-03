from app.repository.repository import DatabaseRepository
from app.services.auth_repo.repository import AuthTokenRepository
from app.services.hash_repo.repository import HashFunctionRepository
from app.services.llm_repo.repository import LLMRepository

class AppConfig:
    """App-wide configuration"""
    def __init__(
        self, 
        db: DatabaseRepository, 
        authrepo: AuthTokenRepository, 
        hashrepo: HashFunctionRepository,
        llmrepo: LLMRepository    
    ):
        self.db = db
        self.authrepo = authrepo
        self.hashrepo = hashrepo
        self.llmrepo = llmrepo