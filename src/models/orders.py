import enum

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class OrdersModel(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str | None]
    telegram: Mapped[str | None]
    product_name: Mapped[str]
    desk_color: Mapped[str]
    frame_color: Mapped[str]
    depth: Mapped[str]
    length: Mapped[str]