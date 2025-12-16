from typing import List
from uuid import UUID

from dto.order_dto import OrderCreate
from entities import Order, order_product
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: UUID) -> Order | None:
        stmt = select(Order).where(Order.id == order_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, count: int, page: int) -> List[Order]:
        stmt = select(Order).offset(count * page).limit(count)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_user(self, user_id: UUID) -> List[Order]:
        stmt = select(Order).where(Order.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, order_data: OrderCreate) -> Order:
        order = Order(user_id=order_data.user_id, address_id=order_data.address_id)
        self.session.add(order)
        await self.session.flush()

        for product_id in order_data.product_ids:
            stmt = order_product.insert().values(
                order_id=order.id, product_id=product_id
            )
            await self.session.execute(stmt)

        await self.session.commit()
        await self.session.refresh(order)

        return order

    async def delete(self, order_id: UUID) -> None:
        stmt = select(Order).where(Order.id == order_id)
        result = await self.session.execute(stmt)
        order = result.scalar_one_or_none()

        if order:
            await self.session.delete(order)
            await self.session.commit()
