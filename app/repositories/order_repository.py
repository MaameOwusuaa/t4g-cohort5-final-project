from sqlalchemy.orm import Session

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        return order

    def get_by_id(self, order_id: int) -> Order | None:
        return (
            self.db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    def get_by_user_id(self, user_id: int) -> list[Order]:
        return (
            self.db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )