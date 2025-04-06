from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Transaction, Card, TransactionType
from schemas import TransactionCreate

@app.post("/transactions/")
async def add_transaction(payload: TransactionCreate, db: AsyncSession = Depends(get_db)):
    # Lookup card_id
    result = await db.execute(select(Card).where(Card.card_number == payload.card_number))
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # Lookup transaction_type_id
    result = await db.execute(select(TransactionType).where(TransactionType.message_label == payload.type_label))
    tx_type = result.scalar_one_or_none()
    if not tx_type:
        raise HTTPException(status_code=404, detail="Transaction type not found")

    new_tx = Transaction(
        amount=payload.amount,
        date=payload.date,
        epos=payload.epos,
        balance=payload.balance,
        card_id=card.id,
        transaction_type_id=tx_type.id
    )

    db.add(new_tx)
    await db.commit()
    return {"message": "Transaction added with card and type ID"}