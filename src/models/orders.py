from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class OrdersModel(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(default=None, nullable=True)
    telegram: Mapped[str] = mapped_column(default=None, nullable=True)
    product_name: Mapped[str] = mapped_column(nullable=False)
    desk_color: Mapped[str] = mapped_column(nullable=False)
    frame_color: Mapped[str] = mapped_column(nullable=False)
    depth: Mapped[str] = mapped_column(nullable=False)
    width: Mapped[str] = mapped_column(nullable=False)