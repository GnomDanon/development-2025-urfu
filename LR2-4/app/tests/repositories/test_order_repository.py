import pytest

from dto.order_dto import OrderCreate
from dto.produc_dto import ProductCreate
from dto.user_dto import UserCreate
from entities import Address
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository


class TestOrderRepository:

    @pytest.mark.asyncio
    async def test_create_order(self, order_repository: OrderRepository, user_repository: UserRepository, product_repository: ProductRepository, session):
        user = await user_repository.create(UserCreate(username="createUser", email="createUser@example.com", description="createUser"))

        address = await Address(user_id=user.id, street="createAddress", city="createAddress", country="createAddress")
        session.add(address)
        await session.commit()
        await session.refresh(address)

        product = await product_repository.create(ProductCreate(name="createProduct", price=100, count=10))

        product_ids = [product.id]

        order = await order_repository.create(OrderCreate(user_id=user.id, address_id=address.id, product_ids=product_ids))

        assert order is not None
        assert order.user_id == user.id
        assert order.address_id == address.id

    @pytest.mark.asyncio
    async def test_get_order_by_id(self, order_repository: OrderRepository, user_repository: UserRepository, session):
        user = await user_repository.create(UserCreate(username="getById", email="getById@example.com", description="getById"))

        address = Address(user_id=user.id, street="getByIdAddress", city="getByIdAddress", country="getByIdAddress")
        session.add(address)
        await session.commit()
        await session.refresh(address)

        order = await order_repository.create(OrderCreate(user_id=user.id, address_id=address.id, product_ids=[]))

        found_order = await order_repository.get_by_id(order.id)

        assert found_order is not None
        assert found_order.user_id == user.id
        assert found_order.address_id == address.id