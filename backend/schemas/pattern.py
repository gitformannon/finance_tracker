from pydantic import BaseModel

class PatternCreate(BaseModel):
    processing_id: int
    processing_name: str
    pattern: str

class PatternOut(PatternCreate):
    id: int

    class Config:
        orm_mode = True
