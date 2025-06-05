from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.individual_orders import SIndividualOrderOut
from src.utils.database import Base
from src.schemas.orders import SOrderOut


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
    sort: Mapped[int | None] = mapped_column(default=500)

    def to_read_model(self) -> SOrderOut:
        return SOrderOut(
            id=self.id,
            username=self.username,
            phone=self.phone,
            email=self.email,
            telegram=self.telegram,
            product_name=self.product_name,
            desk_color=self.desk_color,
            frame_color=self.frame_color,
            depth=self.depth,
            length=self.length,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

class IndividualOrdersModel(Base):
    __tablename__ = 'individual_orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str | None]
    telegram: Mapped[str | None]
    sort: Mapped[int | None] = mapped_column(default=500)

    def to_read_model(self) -> SIndividualOrderOut:
        return SIndividualOrderOut(
            id=self.id,
            username=self.username,
            phone=self.phone,
            email=self.email,
            telegram=self.telegram,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )