from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_items import OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(
        self,
        db: Session,
        repository: OrderRepository,
    ):
        self.db = db
        self.repository = repository

    def create_order(self, user_id: int) -> Order:
        # Get the user's cart
        cart = (
            self.db.query(Cart)
            .filter(Cart.user_id == user_id)
            .first()
        )

        if not cart:
            raise ValueError("Cart not found.")

        # Make sure the cart contains products
        if not cart.cart_items:
            raise ValueError("Cannot create an order from an empty cart.")

        total_amount = Decimal("0.00")

        # Create the order first
        order = Order(
            user_id=user_id,
            total_amount=Decimal("0.00"),
            status="pending",
        )

        self.db.add(order)
        self.db.flush()

        # Create order items
        for cart_item in cart.cart_items:

            product = (
                self.db.query(Product)
                .filter(Product.id == cart_item.product_id)
                .first()
            )

            if not product:
                raise ValueError(
                    f"Product {cart_item.product_id} not found."
                )

            if cart_item.quantity <= 0:
                raise ValueError(
                    f"Invalid quantity for product {product.id}."
                )

            if product.stock_quantity < cart_item.quantity:
                raise ValueError(
                    f"Not enough stock for {product.name}."
                )

            unit_price = Decimal(str(product.price))

            item_total = unit_price * cart_item.quantity

            total_amount += item_total

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=cart_item.quantity,
                unit_price=unit_price,
            )

            self.db.add(order_item)

        # Update the order total
        order.total_amount = total_amount

        self.db.commit()
        self.db.refresh(order)

        return order

    def get_order(
        self,
        order_id: int,
        user_id: int,
    ) -> Order:

        order = self.repository.get_by_id(order_id)

        if not order:
            raise ValueError("Order not found.")

        if order.user_id != user_id:
            raise ValueError("You do not have access to this order.")

        return order

    def get_user_orders(
        self,
        user_id: int,
    ) -> list[Order]:

        return self.repository.get_by_user_id(user_id)