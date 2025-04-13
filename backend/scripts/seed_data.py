import asyncio
from database.session import engine, AsyncSessionLocal
from models import Base
from models.transaction_type import TransactionType
from models.card import Card
from models.pattern import Pattern

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Seed transaction types
        tx_types = [
            TransactionType(message_label="💸 Оплата", internal_type="expense", icon="💸"),
            TransactionType(message_label="🎉 Пополнение", internal_type="income", icon="🎉"),
            TransactionType(message_label="🏧 Снятие наличных", internal_type="cashout", icon="🏧"),
        ]
        db.add_all(tx_types)

        # Seed card
        card = Card(
            number="8600123456789012",
            pan="860012",
            mask="9012",
            name="Uzcard",
            processing_id=1,
            processing_label="Humo",
            balance=500000,
            user_id=1  # assumes a user with id=1 exists
        )
        db.add(card)

        # Seed pattern
        pattern = Pattern(
            processing_id=1,
            processing_name="Humo",
            pattern="💸 Оплата"
        )
        db.add(pattern)

        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())