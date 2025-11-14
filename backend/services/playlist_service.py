"""M3U8 playlist parsing and channel import service"""
import re
import requests
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from backend.models.channel import Channel

class M3U8Parser:
    """Parse M3U8 playlists and extract channel information"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def parse_playlist(self, content: str) -> List[Dict]:
        """
        Parse M3U8 playlist content and extract channels
        
        Format:
        #EXTINF:-1 tvg-id="channel1" tvg-name="Channel Name" tvg-logo="logo.png" group-title="Category",Channel Display Name
        http://stream-url.com/playlist.m3u8
        """
        channels = []
        lines = content.strip().split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for EXTINF lines
            if line.startswith('#EXTINF'):
                # Parse metadata from EXTINF line
                metadata = self._parse_extinf(line)
                
                # Next line should be the stream URL
                if i + 1 < len(lines):
                    stream_url = lines[i + 1].strip()
                    if stream_url and not stream_url.startswith('#'):
                        metadata['stream_url'] = stream_url
                        channels.append(metadata)
                
                i += 2
            else:
                i += 1
        
        return channels
    
    def _parse_extinf(self, line: str) -> Dict:
        """Extract metadata from EXTINF line"""
        metadata = {}
        
        # Extract tvg-id
        tvg_id_match = re.search(r'tvg-id="([^"]*)"', line)
        if tvg_id_match:
            metadata['tvg_id'] = tvg_id_match.group(1)
        
        # Extract tvg-name
        tvg_name_match = re.search(r'tvg-name="([^"]*)"', line)
        if tvg_name_match:
            metadata['tvg_name'] = tvg_name_match.group(1)
        
        # Extract tvg-logo
        tvg_logo_match = re.search(r'tvg-logo="([^"]*)"', line)
        if tvg_logo_match:
            metadata['logo'] = tvg_logo_match.group(1)
        
        # Extract group-title (category)
        group_match = re.search(r'group-title="([^"]*)"', line)
        if group_match:
            metadata['category'] = group_match.group(1)
        
        # Extract channel name (after the last comma)
        name_match = re.search(r',(.+)$', line)
        if name_match:
            metadata['name'] = name_match.group(1).strip()
        
        return metadata
    
    def parse_from_url(self, url: str) -> List[Dict]:
        """Fetch and parse M3U8 playlist from URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return self.parse_playlist(response.text)
        except Exception as e:
            raise Exception(f"Failed to fetch playlist: {str(e)}")
    
    def parse_from_file(self, file_path: str) -> List[Dict]:
        """Parse M3U8 playlist from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_playlist(content)
        except Exception as e:
            raise Exception(f"Failed to read playlist file: {str(e)}")
    
    def import_channels(self, channels: List[Dict]) -> int:
        """Import parsed channels into database"""
        imported = 0
        
        for channel_data in channels:
            # Check if channel already exists
            existing = self.db.query(Channel).filter(
                Channel.stream_url == channel_data.get('stream_url')
            ).first()
            
            if not existing:
                channel = Channel(
                    id=channel_data.get('tvg_id') or f"ch-{imported}",
                    name=channel_data.get('name', 'Unknown'),
                    category=channel_data.get('category', 'Uncategorized'),
                    logo=channel_data.get('logo'),
                    stream_url=channel_data['stream_url'],
                    epg_id=channel_data.get('tvg_id'),
                    is_active=True
                )
                self.db.add(channel)
                imported += 1
        
        self.db.commit()
        return imported


