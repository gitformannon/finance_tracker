import asyncio
from database import AsyncSessionLocal
from models import Card, TransactionType

async def seed():
    async with AsyncSessionLocal() as session:
        session.add_all([
            Card(card_number="*1234", account_id="acc1", description="Main Card"),
            Card(card_number="*5678", account_id="acc2", description="Backup Card"),
            TransactionType(message_label="💸 Оплата", internal_type="expense", icon="💸"),
            TransactionType(message_label="🎉 Пополнение", internal_type="income", icon="🎉"),
            TransactionType(message_label="🏧 Снятие наличных", internal_type="withdrawal", icon="🏧"),
        ])
        await session.commit()

asyncio.run(seed())