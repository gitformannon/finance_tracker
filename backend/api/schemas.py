from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float
    date: datetime
    epos: Optional[str]
    balance: Optional[float]
    card_number: str           # e.g. "*1234"
    type_label: str            # e.g. "💸 Оплата"