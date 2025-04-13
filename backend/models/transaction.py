from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.session import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    epos = Column(String, nullable=True)
    balance = Column(Float, nullable=True)
    date = Column(DateTime(timezone=True), nullable=False)

    card_id = Column(Integer, ForeignKey("cards.id"))
    transaction_type_id = Column(Integer, ForeignKey("transaction_types.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    card = relationship("Card", back_populates="transactions")
    transaction_type = relationship("TransactionType", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
