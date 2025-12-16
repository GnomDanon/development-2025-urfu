from typing import List
from uuid import UUID

from dto.produc_dto import ProductCreate, ProductUpdate
from entities import Product
from repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def get_by_id(self, product_id: UUID) -> Product:
        return await self.product_repository.get_by_id(product_id)

    async def get_all(self, count: int, page: int) -> List[Product]:
        return await self.product_repository.get_all(count, page)

    async def create(self, product: ProductCreate) -> Product:
        return await self.product_repository.create(product)

    async def update(self, product_id: UUID, product: ProductUpdate) -> Product:
        return await self.product_repository.update(product_id, product)

    async def delete(self, product_id: UUID) -> None:
        return await self.product_repository.delete(product_id)