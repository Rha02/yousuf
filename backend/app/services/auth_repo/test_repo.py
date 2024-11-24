
from .repository import AuthTokenRepository


class TestAuthTokenRepository(AuthTokenRepository):
    """Mock token service"""

    def create_token(self, payload: dict) -> str:
        if payload.get("id") == "error":
            raise Exception("Failed to create token")

        return "dummy_token"

    def parse_token(self, token: str) -> dict:
        if token == "bad_token":
            raise Exception("Invalid token")
        
        if token == "nonexistent_user_token":
            return {
                "id": "error",
                "email": "notfound@test.com",
            }

        return {
            "id": "1",
            "email": "dummy.email@test.loc",
        }