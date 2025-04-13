from pydantic import BaseModel
from typing import Optional

class CardCreate(BaseModel):
    number: str
    pan: Optional[str] = None
    mask: Optional[str] = None
    name: Optional[str]
    processing_id: Optional[int]
    processing_label: Optional[str]
    balance: Optional[float]

    def __init__(self, **data):
        super().__init__(**data)
        if not self.pan:
            self.pan = self.number[:6]
        if not self.mask:
            self.mask = self.number[-4:]

class CardOut(CardCreate):
    id: int

    class Config:
        orm_mode = True
