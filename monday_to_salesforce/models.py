#models.py
from sqlalchemy import Column, Integer, String, BigInteger, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class WebhookLog(Base):
    __tablename__ = 'webhook_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    event_type = Column(String)
    board_id = Column(BigInteger)
    item_id = Column(BigInteger)
    column_id = Column(String)
    new_value = Column(Text)
    status = Column(String)
    error_message = Column(Text, nullable=True)