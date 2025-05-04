from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class ProductsModel(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    first_image: Mapped[str]
    second_image: Mapped[str]
    third_image: Mapped[str]
