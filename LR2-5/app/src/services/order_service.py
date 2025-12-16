from typing import List
from uuid import UUID

from dto.order_dto import OrderCreate
from repositories.order_repository import OrderRepository
from src.entities import Order


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def get_by_id(self, order_id: UUID) -> Order:
        return await self.order_repository.get_by_id(order_id)

    async def get_all(self, count: int, page: int) -> List[Order]:
        return await self.order_repository.get_all(count, page)

    async def get_by_user(self, user_id: UUID) -> List[Order]:
        return await self.order_repository.get_by_user(user_id)

    async def create(self, order: OrderCreate) -> Order:
        return await self.order_repository.create(order)

    async def delete(self, order_id: UUID) -> None:
        return await self.order_repository.delete(order_id)
