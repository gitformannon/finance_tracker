from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="user")
    cards = relationship("Card", back_populates="user")
