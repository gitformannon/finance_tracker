from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True, nullable=False)
    account_id = Column(String, nullable=False)
    description = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="card")


class TransactionType(Base):
    __tablename__ = "transaction_types"

    id = Column(Integer, primary_key=True, index=True)
    message_label = Column(String, unique=True, nullable=False)
    internal_type = Column(String, nullable=False)
    icon = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="transaction_type")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    epos = Column(String, nullable=True)
    balance = Column(Float, nullable=True)

    card_id = Column(Integer, ForeignKey("cards.id"))
    transaction_type_id = Column(Integer, ForeignKey("transaction_types.id"))

    card = relationship("Card", back_populates="transactions")
    transaction_type = relationship("TransactionType", back_populates="transactions")