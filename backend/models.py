from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False)  # full card number (if needed)
    pan = Column(String, nullable=True)      # first 4–6 digits
    mask = Column(String, nullable=False)    # last 4 digits
    name = Column(String, nullable=True)
    processing_id = Column(Integer, nullable=True)
    processing_label = Column(String, nullable=True)
    balance = Column(Float, nullable=True)

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


class Pattern(Base):
    __tablename__ = "patterns"

    id = Column(Integer, primary_key=True, index=True)
    processing_id = Column(Integer, nullable=False)
    processing_name = Column(String, nullable=False)
    pattern = Column(String, nullable=False)