from sqlalchemy import Column, Integer, String, Text
from database.session import Base

class MessageTemplate(Base):
    __tablename__ = "message_templates"

    id = Column(Integer, primary_key=True, index=True)
    processing_id = Column(Integer, index=True)
    message_pattern = Column(Text)