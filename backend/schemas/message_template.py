from pydantic import BaseModel

class MessageTemplateBase(BaseModel):
    processing_id: int
    message_pattern: str

class MessageTemplateCreate(MessageTemplateBase):
    pass

class MessageTemplateInDB(MessageTemplateBase):
    id: int

    class Config:
        from_attributes = True

