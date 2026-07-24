from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
