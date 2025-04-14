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

        existing_templates = {tpl.name for tpl in (await db.execute(select(MessageTemplate))).scalars().all()}

        templates_to_add = [
            {
                "name": "uzcard_template",
                "pattern": "💸 Platezh\n📍 CHAKANAPAY KREDIT SUNDIRISH, UZ\n➖ {amount} UZS\n💳 ***{card_mask}\n🕓 {date}\n💵 {balance} UZS",
                "processing_id": 2
            },
            {
                "name": "humo_template",
                "pattern": "💸 Оплата\n➖ {amount} UZS\n⚠️ Комиссия: {commission} UZS\n📍 {epos}\n💳 VISA *{card_mask}\n🕓 {date}\n💰 {balance} UZS",
                "processing_id": 1
            }
        ]

        for tpl in templates_to_add:
            if tpl["name"] not in existing_templates:
                db.add(MessageTemplate(**tpl))

        await db.commit()

if __name__ == "__main__":
    asyncio.run(seed())