from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)

        return payment

    def get_by_id(self, payment_id: int) -> Payment | None:
        return (
            self.db.query(Payment)
            .filter(Payment.id == payment_id)
            .first()
        )

    def get_by_order_id(self, order_id: int) -> Payment | None:
        return (
            self.db.query(Payment)
            .filter(Payment.order_id == order_id)
            .first()
        )

    def get_by_transaction_reference(
        self,
        reference: str,
    ) -> Payment | None:
        return (
            self.db.query(Payment)
            .filter(
                Payment.transaction_reference == reference
            )
            .first()
        )

    def update(self, payment: Payment) -> Payment:
        self.db.commit()
        self.db.refresh(payment)

        return payment