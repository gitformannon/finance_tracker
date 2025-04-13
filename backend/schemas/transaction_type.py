from pydantic import BaseModel
from typing import Optional

class TransactionTypeCreate(BaseModel):
    message_label: str
    internal_type: Optional[str]
    icon: Optional[str]

class TransactionTypeOut(TransactionTypeCreate):
    id: int

    class Config:
        orm_mode = True
