from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


# добавляем таблицу клиентов
class CustomerOrm(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True)
