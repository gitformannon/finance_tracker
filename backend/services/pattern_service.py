from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import MessageTemplate
from schemas.message_template import MessageTemplateCreate

async def get_all_templates(db: AsyncSession) -> list[MessageTemplate]:
    result = await db.execute(select(MessageTemplate))
    return result.scalars().all()

async def create_template(template_data: MessageTemplateCreate, db: AsyncSession) -> MessageTemplate:
    new_template = MessageTemplate(**template_data.dict())
    db.add(new_template)
    await db.commit()
    await db.refresh(new_template)
    return new_template

async def find_matching_template(message: str, db: AsyncSession) -> MessageTemplate | None:
    result = await db.execute(select(MessageTemplate))
    templates = result.scalars().all()
    for template in templates:
        if template.message_template in message:
            return template
    return None
