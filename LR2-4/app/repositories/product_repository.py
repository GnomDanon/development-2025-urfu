from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dto.produc_dto import ProductCreate, ProductUpdate
from entities import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: UUID) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, count: int, page: int) -> List[Product]:
        stmt = select(Product).offset(count * page).limit(count)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.model_dump())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update(self, product_id: UUID, product_data: ProductUpdate) -> Product:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()

        if not product:
            raise ValueError(f"Product {product_id} not found")

        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product, key, value)

        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete(self, product_id: UUID) -> None:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        product = result.scalar_one_or_none()

        if product:
            await self.session.delete(product)
            await self.session.commit()