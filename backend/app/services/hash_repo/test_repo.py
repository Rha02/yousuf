from .repository import HashFunctionRepository

class TestHashRepository(HashFunctionRepository):
    """Test implementation of HashFunctionRepository"""

    def hash(self, value: str) -> str:
        if value == "BadPassword1!":
            raise Exception("Hashing failed");
        
        return f"hash({value})"
    
    def compare(self, value: str, hashed_value: str) -> bool:
        return hashed_value == f"hash({value})"