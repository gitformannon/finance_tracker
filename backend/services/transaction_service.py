from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Transaction, TransactionType, Card
from schemas.transaction import TransactionCreate
from models import User

async def create_transaction(data: TransactionCreate, user: User, db: AsyncSession) -> Transaction:
    result = await db.execute(select(Card).where(Card.mask == data.card_number[-4:], Card.user_id == user.id))
    card = result.scalar_one_or_none()
    if not card:
        raise ValueError("Card not found")

    result = await db.execute(select(TransactionType).where(TransactionType.message_label == data.type_label))
    tx_type = result.scalar_one_or_none()
    if not tx_type:
        raise ValueError("Transaction type not found")

    new_transaction = Transaction(
        amount=data.amount,
        epos=data.epos,
        balance=data.balance,
        date=data.date,
        card_id=card.id,
        transaction_type_id=tx_type.id,
        user_id=user.id
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

async def get_transactions_for_user(user_id: int, db: AsyncSession) -> list[Transaction]:
    result = await db.execute(select(Transaction).where(Transaction.user_id == user_id))
    return result.scalars().all()
