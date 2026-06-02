from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class CodeHistory(Base):
    __tablename__ = "code_history"

    id = Column(Integer, primary_key=True, index=True)
    code_type = Column(String, index=True) 
    data = Column(String)                 
    created_at = Column(DateTime(timezone=True), server_default=func.now())