"""API client for backend communication"""

import httpx
from typing import Optional


class APIClient:
    """Client for communicating with FastAPI backend"""

    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url)

    def get_channels(self) -> list[dict]:
        """Fetch all channels"""
        response = self.client.get("/api/v1/channels")
        return response.json()

    def get_stream_url(self, channel_id: str) -> dict:
        """Get stream URL for channel"""
        response = self.client.get(f"/api/v1/stream/{channel_id}")
        return response.json()

    def get_epg(self, channel_id: str) -> dict:
        """Get EPG data for channel"""
        response = self.client.get(f"/api/v1/epg/{channel_id}")
        return response.json()
