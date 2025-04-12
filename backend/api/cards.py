from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.session import get_db
from core.security import get_current_user
from schemas import CardCreate, CardOut
from models import Card, User

router = APIRouter()

@router.get("/", response_model=list[CardOut], summary="Get all cards for the user")
async def get_cards(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Card).where(Card.user_id == current_user.id))
    return result.scalars().all()

@router.post("/", response_model=CardOut, summary="Add a new card")
async def create_card(card_data: CardCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = await db.execute(select(Card).where(Card.mask == card_data.mask, Card.user_id == current_user.id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Card already exists")

    new_card = Card(**card_data.dict(), user_id=current_user.id)
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card
