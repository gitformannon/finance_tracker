from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.session import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)
    pan = Column(String, nullable=True)  # First 4–6 digits
    mask = Column(String, nullable=False)  # Last 4 digits
    name = Column(String, nullable=True)
    processing_id = Column(Integer, nullable=True)
    processing_label = Column(String, nullable=True)
    balance = Column(Float, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cards")

    transactions = relationship("Transaction", back_populates="card")
