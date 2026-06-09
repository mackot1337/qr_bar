from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class CodeHistory(Base):
    __tablename__ = "code_history"

    id = Column(Integer, primary_key=True, index=True)
    code_type = Column(String, index=True) 
    data = Column(String)                 

    fill_color = Column(String, default="black")
    back_color = Column(String, default="white")
    barcode_type = Column(String, default="code128")

    image_base64 = Column(Text, nullable=True)
    logo_base64 = Column(Text, nullable=True)
    logo_name = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())