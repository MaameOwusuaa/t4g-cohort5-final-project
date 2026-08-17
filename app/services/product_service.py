from fastapi import HTTPException, status

from app.models.product import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.products import ProductCreate, ProductUpdate


class ProductService:
    def __init__(
        self,
        product_repository: ProductRepository,
        category_repository: CategoryRepository,
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def create_product(self, product_data: ProductCreate):
        category = self.category_repository.get_by_id(
            product_data.category_id
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found.",
            )

        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock_quantity=product_data.stock_quantity,
            image_url=product_data.image_url,
            category_id=product_data.category_id,
        )

        return self.product_repository.create(product)

    def get_all_products(self):
        return self.product_repository.get_all()

    def get_product_by_id(self, product_id: int):
        product = self.product_repository.get_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        return product

    def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate,
    ):
        product = self.get_product_by_id(product_id)

        update_data = product_data.model_dump(exclude_unset=True)

        if (
            "category_id" in update_data
            and update_data["category_id"] is not None
        ):
            category = self.category_repository.get_by_id(
                update_data["category_id"]
            )

            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Category not found.",
                )

        for field, value in update_data.items():
            setattr(product, field, value)

        self.product_repository.update()

        return product

    def delete_product(self, product_id: int):
        product = self.get_product_by_id(product_id)

        self.product_repository.delete(product)

        return {
            "message": "Product deleted successfully."
        }