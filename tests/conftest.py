import pytest

from database import Base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from schemas.customer import (
    CreateCustomerSchema,
    UpdateCustomerSchema,
)

TEST_DB_URI = 'sqlite+aiosqlite:///microshop-test.db'


@pytest.fixture(scope='session')
async def db_session() -> AsyncSession:
    engine = create_async_engine(TEST_DB_URI)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncSession = async_sessionmaker(bind=engine)
    async with AsyncSession() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



@pytest.fixture
def create_customer() -> CreateCustomerSchema:
    return CreateCustomerSchema(
        first_name='Иван',
        last_name='Иванович',
        email='ivan@ivan.com',
        phone_number=9999999999,
    )


@pytest.fixture
def update_customer_full() -> UpdateCustomerSchema:
    return UpdateCustomerSchema(
        first_name='Олег',
        last_name='Олегович',
        email='qwerty@qwerty.com',
        phone_number=9888888888,
    )


@pytest.fixture
def update_customer_partial() -> UpdateCustomerSchema:
    return UpdateCustomerSchema(
        email='qwerty@qwerty.com',
        phone_number=9888888888,
    )

