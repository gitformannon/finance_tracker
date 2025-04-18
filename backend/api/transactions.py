from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.session import get_db
from models import Card, TransactionType, Transaction
from schemas import TransactionCreate
from core.security import get_current_user
from models import User
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/", summary="Create a new transaction")
async def create_transaction(
    payload: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"🔍 Incoming payload: {payload}")

    result = await db.execute(select(Card).where(Card.mask == payload.card_number[-4:]))
    card = result.scalar_one_or_none()
    if not card:
        logger.warning(f"❌ Card not found with mask: {payload.card_number[-4:]}")
        raise HTTPException(status_code=404, detail="Card not found")

    result = await db.execute(select(TransactionType).where(TransactionType.message_label == payload.type_label))
    tx_type = result.scalar_one_or_none()
    if not tx_type:
        logger.warning(f"❌ Transaction type not found for label: {payload.type_label}")
        raise HTTPException(status_code=404, detail="Transaction type not found")

    new_tx = Transaction(
        amount=payload.amount,
        date=payload.date,
        epos=payload.epos,
        balance=payload.balance,
        card_id=card.id,
        transaction_type_id=tx_type.id,
        user_id=current_user.id
    )

    db.add(new_tx)
    await db.commit()
    logger.info("✅ Transaction successfully created.")
    return {"message": "Transaction added"}

@router.get("/", summary="Get all transactions")
async def get_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Transaction).where(Transaction.user_id == current_user.id)
    )
    transactions = result.scalars().all()
    return transactions
