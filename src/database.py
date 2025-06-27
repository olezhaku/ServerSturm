from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from schemas import UserSchema


# settings
engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# models
class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(256), nullable=False)


# requests
async def have_users() -> User | None:
    async with async_session() as session:
        result = await session.execute(select(User))
        user = result.scalars().first()

        return user


async def create_user(creds: UserSchema) -> bool:
    async with async_session() as session:
        user = User(**creds.model_dump())
        session.add(user)
        await session.commit()

        return True


async def check_user(username: str) -> User | None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalars().first()

        return user
