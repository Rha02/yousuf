from app.repository.repository import DatabaseRepository
from app.services.auth_repo.repository import AuthTokenRepository

class AppConfig:
    """App-wide configuration"""
    def __init__(self, db: DatabaseRepository, authrepo: AuthTokenRepository):
        self.db = db
        self.authrepo = authrepo