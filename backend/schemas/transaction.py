from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionCreate(BaseModel):
    amount: float
    epos: Optional[str]
    balance: Optional[float]
    date: datetime
    card_number: str
    type_label: str

class TransactionOut(BaseModel):
    id: int
    amount: float
    epos: Optional[str]
    balance: Optional[float]
    date: datetime
    card_id: int
    transaction_type_id: int
    user_id: int

    class Config:
        orm_mode = True
