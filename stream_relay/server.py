"""Stream relay server"""
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Stream Relay Service")

@app.get("/hls/{channel_id}/playlist.m3u8")
async def get_playlist(channel_id: str):
    """Generate HLS playlist"""
    # TODO: Implement HLS generation
    return {"message": "HLS playlist"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
