from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Cart(BaseModel):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    user = relationship(
        "User",
        back_populates="cart",
    )

    cart_items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )