from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Card
from schemas.card import CardCreate
from models import User

async def get_card_by_mask(mask: str, user_id: int, db: AsyncSession) -> Card | None:
    result = await db.execute(select(Card).where(Card.mask == mask, Card.user_id == user_id))
    return result.scalar_one_or_none()

async def get_all_cards_for_user(user_id: int, db: AsyncSession) -> list[Card]:
    result = await db.execute(select(Card).where(Card.user_id == user_id))
    return result.scalars().all()

async def create_card(card_data: CardCreate, user: User, db: AsyncSession) -> Card:
    pan = card_data.number[:6]
    mask = card_data.number[-4:]
    card_dict = card_data.dict()
    card_dict["pan"] = pan
    card_dict["mask"] = mask
    new_card = Card(**card_dict, user_id=user.id)
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card
