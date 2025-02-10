from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# создаем движок который управляет сессией в асинхронном режиме

engine = create_async_engine("sqlite+aiosqlite:///microshop.db", echo=True)


class Base(DeclarativeBase):
    pass


# создаем асинхронную сессию
AsyncSession = async_sessionmaker(bind=engine)


# Генератор дял сессии
async def get_db_session():
    async with AsyncSession() as session:
        yield session
