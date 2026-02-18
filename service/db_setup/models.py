from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from service.user_schema import User

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default="1"
    )

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        """Convert domain entity to persistence model"""
        return cls(
            id=user.id,
            username=user.username,
            password=user.password,
            active=1 if user.active else 0,
        )

    def to_domain(self) -> User:
        """Convert persistence model to domain entity"""
        return User(
            id=self.id,
            username=self.username,
            password=self.password,
            active=bool(self.active),
        )
