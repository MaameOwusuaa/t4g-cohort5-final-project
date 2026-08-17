from fastapi import HTTPException, status

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.repositories.cart_repositories import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import CartItemCreate, CartItemUpdate


class CartService:
    def __init__(
        self,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
    ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def get_or_create_cart(self, user_id: int):
        cart = self.cart_repository.get_cart_by_user_id(user_id)

        if not cart:
            cart = Cart(user_id=user_id)
            cart = self.cart_repository.create_cart(cart)

        return cart

    def add_item(
        self,
        user_id: int,
        item_data: CartItemCreate,
    ):
        cart = self.get_or_create_cart(user_id)

        product = self.product_repository.get_by_id(
            item_data.product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        if product.stock_quantity < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock.",
            )

        existing_item = self.cart_repository.get_cart_item(
            cart.id,
            item_data.product_id,
        )

        if existing_item:
            new_quantity = (
                existing_item.quantity + item_data.quantity
            )

            if product.stock_quantity < new_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Insufficient stock.",
                )

            existing_item.quantity = new_quantity

            return self.cart_repository.update_cart_item(
                existing_item
            )

        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
        )

        return self.cart_repository.add_cart_item(
            cart_item
        )

    def get_cart(self, user_id: int):
        return self.get_or_create_cart(user_id)

    def update_item(
        self,
        user_id: int,
        product_id: int,
        item_data: CartItemUpdate,
    ):
        cart = self.get_or_create_cart(user_id)

        cart_item = self.cart_repository.get_cart_item(
            cart.id,
            product_id,
        )

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product is not in the cart.",
            )

        product = self.product_repository.get_by_id(
            product_id
        )

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        if product.stock_quantity < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock.",
            )

        cart_item.quantity = item_data.quantity

        return self.cart_repository.update_cart_item(
            cart_item
        )

    def remove_item(
        self,
        user_id: int,
        product_id: int,
    ):
        cart = self.get_or_create_cart(user_id)

        cart_item = self.cart_repository.get_cart_item(
            cart.id,
            product_id,
        )

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product is not in the cart.",
            )

        self.cart_repository.delete_cart_item(
            cart_item
        )

        return {
            "message": "Product removed from cart successfully."
        }

    def clear_cart(self, user_id: int):
        cart = self.get_or_create_cart(user_id)

        self.cart_repository.clear_cart(cart)

        return {
            "message": "Cart cleared successfully."
        }