"""EPG API endpoints"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/epg", tags=["epg"])

@router.get("/{channel_id}")
async def get_epg(channel_id: str):
    """Get EPG data for channel"""
    # TODO: Implement
    return {
        "current": {},
        "upcoming": []
    }
