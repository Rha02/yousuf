from fastapi import APIRouter

def create_router(db: any):
    """Create an instance of the FastAPI application"""
    router = APIRouter()

    @router.post("/login")
    async def login():
        return {"message": "Login"}

    @router.post("/register")
    async def register():
        return {"message": "Register"}

    @router.post("/logout")
    async def logout():
        return {"message": "Logout"}

    @router.post("/user")
    async def user():
        return {"message": "User"}

    return router