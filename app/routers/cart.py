from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.repositories.cart_repositories import CartRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.cart import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
    CartResponse,
)
from app.services.cart_service import CartService


router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


def get_cart_service(
    db: Session = Depends(get_db),
):
    cart_repository = CartRepository(db)
    product_repository = ProductRepository(db)

    return CartService(
        cart_repository,
        product_repository,
    )


@router.get(
    "",
    response_model=CartResponse,
)
def get_cart(
    current_user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
):
    return service.get_cart(current_user.id)


@router.post(
    "/items",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_item_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
):
    return service.add_item(
        current_user.id,
        item,
    )


@router.put(
    "/items/{product_id}",
    response_model=CartItemResponse,
)
def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
):
    return service.update_item(
        current_user.id,
        product_id,
        item,
    )


@router.delete(
    "/items/{product_id}",
)
def remove_cart_item(
    product_id: int,
    current_user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
):
    return service.remove_item(
        current_user.id,
        product_id,
    )


@router.delete(
    "",
)
def clear_cart(
    current_user: User = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
):
    return service.clear_cart(current_user.id)