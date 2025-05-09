from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    desk_colors: Mapped[list["DeskColors"]] = relationship(
        secondary="product_desk_color",
        back_populates="products"
    )
    frame_colors: Mapped[list["FrameColors"]] = relationship(
        secondary="product_frame_color",
        back_populates="products"
    )
    length: Mapped[list["Length"]] = relationship(
        secondary="product_length",
        back_populates="products"
    )
    depth: Mapped[list["Depth"]] = relationship(
        secondary="product_depth",
        back_populates="products"
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

class FrameColors(Base):
    __tablename__ = 'frame_colors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    products: Mapped[list["ProductsModel"]] = relationship(
        secondary="product_frame_color",
        back_populates="frame_colors"
    )

class Length(Base):
    __tablename__ = 'length'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]

    products: Mapped[list["ProductsModel"]] = relationship(
        secondary="product_length",
        back_populates="length"
    )

class Depth(Base):
    __tablename__ = 'depth'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]

    products: Mapped[list["ProductsModel"]] = relationship(
        secondary="product_depth",
        back_populates="depth"
    )