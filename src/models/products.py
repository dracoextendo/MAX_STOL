from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.schemas.products import SProductOut
from src.utils.database import Base
from src.schemas.settings import SDeskColorOut, SFrameColorOut, SLengthOut, SDepthOut


class ProductsModel(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    first_image: Mapped[str]
    second_image: Mapped[str]
    third_image: Mapped[str]
    desk_colors: Mapped[list["DeskColors"]] = relationship(
        secondary="product_desk_color",
        back_populates="products"
    )
    frame_colors: Mapped[list["FrameColors"]] = relationship(
        secondary="product_frame_color",
        back_populates="products"
    )
    lengths: Mapped[list["Length"]] = relationship(
        secondary="product_length",
        back_populates="products"
    )
    depths: Mapped[list["Depth"]] = relationship(
        secondary="product_depth",
        back_populates="products"
    )
    sort: Mapped[int | None] = mapped_column(default=500)
    is_active: Mapped[bool| None] = mapped_column(default=True)

    def to_read_model(self) -> SProductOut:
        return SProductOut(
                id=self.id,
                sort=self.sort,
                is_active=self.is_active,
                name=self.name,
                description=self.description,
                price=self.price,
                first_image=self.first_image,
                second_image=self.second_image,
                third_image=self.third_image,
                created_at=self.created_at,
                updated_at=self.updated_at,
            )

class ProductDeskColor(Base):
    __tablename__ = 'product_desk_color'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    desk_color_id: Mapped[int] = mapped_column(ForeignKey("desk_colors.id"))

class ProductFrameColor(Base):
    __tablename__ = 'product_frame_color'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    frame_color_id: Mapped[int] = mapped_column(ForeignKey("frame_colors.id"))

class ProductLength(Base):
    __tablename__ = 'product_length'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    length_id: Mapped[int] = mapped_column(ForeignKey("length.id"))

class ProductDepth(Base):
    __tablename__ = 'product_depth'
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    depth_id: Mapped[int] = mapped_column(ForeignKey("depth.id"))

class DeskColors(Base):
    __tablename__ = 'desk_colors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    products: Mapped[list["ProductsModel"]] = relationship(
        secondary="product_desk_color",
        back_populates="desk_colors"
    )
    sort: Mapped[int | None] = mapped_column(default=500)

    def to_read_model(self) -> SDeskColorOut:
        return SDeskColorOut(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
            sort=self.sort,
        )

class FrameColors(Base):
    __tablename__ = 'frame_colors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    products: Mapped[list["ProductsModel"]] = relationship(
        secondary="product_frame_color",
        back_populates="frame_colors"
    )
    sort: Mapped[int | None] = mapped_column(default=500)

    def to_read_model(self) -> SFrameColorOut:
        return SFrameColorOut(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
            sort=self.sort,
        )

class Length(Base):
    __tablename__ = 'length'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]

    products: Mapped[list["ProductsModel"]] = relationship(
        secondary="product_length",
        back_populates="lengths"
    )
    sort: Mapped[int | None] = mapped_column(default=500)

    def to_read_model(self) -> SLengthOut:
        return SLengthOut(
            id=self.id,
            value=self.value,
            created_at=self.created_at,
            updated_at=self.updated_at,
            sort=self.sort,
        )

class Depth(Base):
    __tablename__ = 'depth'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]

    products: Mapped[list["ProductsModel"]] = relationship(
        secondary="product_depth",
        back_populates="depths"
    )
    sort: Mapped[int | None] = mapped_column(default=500)

    def to_read_model(self) -> SDepthOut:
        return SDepthOut(
            id=self.id,
            value=self.value,
            created_at=self.created_at,
            updated_at=self.updated_at,
            sort=self.sort,
        )