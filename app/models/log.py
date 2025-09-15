# models/log.py
from sqlalchemy import Column,  String, DateTime, Text
from datetime import datetime
from .base import Base


class LogModel(Base):
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    route = Column(String, nullable=False)
    function_name = Column(String, nullable=False)
    level = Column(String, nullable=False)
    message = Column(Text, nullable=False)