import asyncio
from database.session import engine, AsyncSessionLocal
from models import Base
from models.transaction_type import TransactionType
from models.card import Card
from models.message_template import MessageTemplate
from sqlalchemy import select

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(TransactionType))
        existing_labels = {tx_type.message_label for tx_type in result.scalars().all()}

        tx_types_to_add = [
            {"message_label": "💸 Оплата", "internal_type": "expense", "icon": "💸", "processing_id": 1},
            {"message_label": "🎉 Пополнение", "internal_type": "income", "icon": "🎉", "processing_id": 1},
            {"message_label": "🏧 Снятие наличных", "internal_type": "cashout", "icon": "🏧", "processing_id": 1},
        ]

        for tx in tx_types_to_add:
            if tx["message_label"] not in existing_labels:
                db.add(TransactionType(**tx))

        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())