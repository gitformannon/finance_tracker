from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User
from schemas.auth import UserCreate
from core.auth import hash_password

async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
