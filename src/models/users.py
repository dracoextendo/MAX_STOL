from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.users import SUserOut
from src.utils.database import Base


class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    def to_read_model(self) -> SUserOut:
        return SUserOut(
            id=self.id,
            username=self.username,
            email=self.email,
        )