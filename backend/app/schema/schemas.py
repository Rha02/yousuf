from app.models.user import User

def user_serializer(user: User) -> dict:
    return {
        "email": user.email,
        "password": user.password,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

def list_serial(users: list[User]) -> list[dict]:
    return [user_serializer(user) for user in users]