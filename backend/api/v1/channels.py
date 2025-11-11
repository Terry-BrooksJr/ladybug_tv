"""Channel API endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db

router = APIRouter(prefix="/api/v1/channels", tags=["channels"])

@router.get("/")
async def get_channels(db: Session = Depends(get_db)):
    """Get all channels"""
    # TODO: Implement
    return []

@router.get("/{channel_id}")
async def get_channel(channel_id: str, db: Session = Depends(get_db)):
    """Get single channel"""
    # TODO: Implement
    return {}
