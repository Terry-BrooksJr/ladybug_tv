"""Playlist import API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from backend.database import get_db
from backend.services.playlist_service import M3U8Parser

router = APIRouter(prefix="/api/v1/playlists", tags=["playlists"])

class PlaylistURL(BaseModel):
    url: HttpUrl

@router.post("/import/url")
async def import_from_url(
    playlist: PlaylistURL,
    db: Session = Depends(get_db)
):
    """Import channels from M3U8 playlist URL"""
    parser = M3U8Parser(db)
    
    try:
        channels = parser.parse_from_url(str(playlist.url))
        imported = parser.import_channels(channels)
        
        return {
            "message": f"Successfully imported {imported} channels",
            "total_parsed": len(channels),
            "imported": imported
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.post("/import/file")
async def import_from_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import channels from uploaded M3U8 file"""
    if not file.filename.endswith(('.m3u', '.m3u8')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .m3u or .m3u8 files allowed"
        )
    
    parser = M3U8Parser(db)
    
    try:
        content = await file.read()
        channels = parser.parse_playlist(content.decode('utf-8'))
        imported = parser.import_channels(channels)
        
        return {
            "message": f"Successfully imported {imported} channels",
            "total_parsed": len(channels),
            "imported": imported
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/parse/preview")
async def preview_playlist(url: str):
    """Preview channels in a playlist without importing"""
    parser = M3U8Parser(None)  # No DB needed for preview

    try:
        channels = parser.parse_from_url(url)
        return {
            "total_channels": len(channels),
            "channels": channels[:20],
            "categories": list(
                {ch.get('category', 'Uncategorized') for ch in channels}
            ),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e