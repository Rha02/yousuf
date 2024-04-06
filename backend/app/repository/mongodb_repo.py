from .repository import DatabaseRepository
from app.models.user import User
from driver.driver import MongoDB

class MongoDBRepository(DatabaseRepository):
    """MongoDB implementation of a database repository"""

    def __init__(self, client: MongoDB):
        self.db = client.db

    def get_user_by_email(self, email: str) -> User:
        return self.db.users.find_one({"email": email})
    
    def get_user_by_id(self, user_id: int) -> User:
        return self.db.users.find_one({"id": user_id})
    
    def create_user(self, user: User) -> User:
        self.db.users.insert_one(user.model_dump())
        return user