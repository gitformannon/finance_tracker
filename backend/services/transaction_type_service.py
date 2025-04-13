from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import TransactionType
from schemas.transaction_type import TransactionTypeCreate

async def get_transaction_type_by_label(label: str, db: AsyncSession) -> TransactionType | None:
    result = await db.execute(select(TransactionType).where(TransactionType.message_label == label))
    return result.scalar_one_or_none()

async def create_transaction_type(data: TransactionTypeCreate, db: AsyncSession) -> TransactionType:
    new_type = TransactionType(**data.dict())
    db.add(new_type)
    await db.commit()
    await db.refresh(new_type)
    return new_type

async def get_all_transaction_types(db: AsyncSession) -> list[TransactionType]:
    result = await db.execute(select(TransactionType))
    return result.scalars().all()
