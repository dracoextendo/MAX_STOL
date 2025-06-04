from sqlalchemy.orm import Mapped, mapped_column

from src.utils.database import Base


class ContentModel(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(primary_key=True)
    banner_first_frame_title: Mapped[str | None]
    banner_first_frame_description: Mapped[str | None]
    banner_first_frame_button: Mapped[str | None]
    banner_second_frame_title: Mapped[str | None]
    banner_second_frame_description: Mapped[str | None]
    banner_second_frame_button: Mapped[str | None]
    catalog_title: Mapped[str | None]
    catalog_description: Mapped[str | None]
    reasons_title: Mapped[str | None]
    reasons_description: Mapped[str | None]
    reasons_first_title: Mapped[str | None]
    reasons_first_description: Mapped[str | None]
    reasons_second_title: Mapped[str | None]
    reasons_second_description: Mapped[str | None]
    reasons_third_title: Mapped[str | None]
    reasons_third_description: Mapped[str | None]
    reasons_four_title: Mapped[str | None]
    reasons_four_description: Mapped[str | None]
    individual_order_sub: Mapped[str | None]
    individual_order_title: Mapped[str | None]
    individual_order_description: Mapped[str | None]
    individual_order_button: Mapped[str | None]
    steps_title: Mapped[str | None]
    steps_first_title: Mapped[str | None]
    steps_first_description: Mapped[str | None]
    steps_second_title: Mapped[str | None]
    steps_second_description: Mapped[str | None]
    steps_third_title: Mapped[str | None]
    steps_third_description: Mapped[str | None]
    steps_four_title: Mapped[str | None]
    steps_four_description: Mapped[str | None]
    contacts_title: Mapped[str | None]
    contacts_phone: Mapped[str | None]
    contacts_email: Mapped[str | None]
    contacts_address: Mapped[str | None]
    contacts_telegram: Mapped[str | None]