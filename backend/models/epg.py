"""EPG database model"""
from sqlalchemy import Column, String, Integer, DateTime
from backend.database import Base

class EPGProgram(Base):
    __tablename__ = "epg_programs"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
