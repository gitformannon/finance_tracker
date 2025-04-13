from sqlalchemy import Column, Integer, String
from database.session import Base

class Pattern(Base):
    __tablename__ = "patterns"

    id = Column(Integer, primary_key=True, index=True)
    processing_id = Column(Integer, nullable=False)
    processing_name = Column(String, nullable=False)
    pattern = Column(String, nullable=False)
