"""Stream API endpoints"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/stream", tags=["streams"])

@router.get("/{channel_id}")
async def get_stream_url(channel_id: str):
    """Get stream URL for channel"""
    # TODO: Implement
    return {"stream_url": f"http://localhost:8002/hls/{channel_id}/playlist.m3u8"}
