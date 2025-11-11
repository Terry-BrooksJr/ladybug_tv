"""Authentication API endpoints"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login")
async def login(email: str, password: str):
    """User login"""
    # TODO: Implement
    return {"access_token": "token", "token_type": "bearer"}

@router.post("/register")
async def register(email: str, password: str):
    """User registration"""
    # TODO: Implement
    return {"message": "User created"}
