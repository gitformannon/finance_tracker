from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.session import Base

class TransactionType(Base):
    __tablename__ = "transaction_types"

    id = Column(Integer, primary_key=True, index=True)
    message_label = Column(String, nullable=False, unique=True)  # e.g. 💸 Оплата
    internal_type = Column(String, nullable=True)  # e.g. expense, income
    icon = Column(String, nullable=True)  # optional emoji or icon
    processing_id = Column(Integer, nullable=True)

    transactions = relationship("Transaction", back_populates="transaction_type")
