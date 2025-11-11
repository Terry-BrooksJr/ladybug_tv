"""Channel database model"""
from sqlalchemy import Column, String, Integer, Boolean
from backend.database import Base

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    logo = Column(String)
    stream_url = Column(String, nullable=False)
    epg_id = Column(String)
    is_active = Column(Boolean, default=True)
