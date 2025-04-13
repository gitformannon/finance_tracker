from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Pattern
from schemas.pattern import PatternCreate

async def get_all_patterns(db: AsyncSession) -> list[Pattern]:
    result = await db.execute(select(Pattern))
    return result.scalars().all()

async def create_pattern(pattern_data: PatternCreate, db: AsyncSession) -> Pattern:
    new_pattern = Pattern(**pattern_data.dict())
    db.add(new_pattern)
    await db.commit()
    await db.refresh(new_pattern)
    return new_pattern

async def find_matching_pattern(message: str, db: AsyncSession) -> Pattern | None:
    result = await db.execute(select(Pattern))
    patterns = result.scalars().all()
    for pattern in patterns:
        if pattern.pattern in message:
            return pattern
    return None
