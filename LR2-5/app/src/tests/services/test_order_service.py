from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
import pytest_asyncio
from dto.order_dto import OrderCreate
from entities import Order
from repositories.order_repository import OrderRepository
from services.order_service import OrderService


class TestOrderService:
    @pytest_asyncio.fixture
    def mock_order_repository(self):
        return AsyncMock(spec=OrderRepository)

    @pytest_asyncio.fixture
    def order_service(self, mock_order_repository):
        return OrderService(order_repository=mock_order_repository)

    @pytest_asyncio.fixture
    def sample_uuid(self):
        return UUID("11111111-2222-3333-4444-555555555555")

    @pytest_asyncio.fixture
    def another_sample_uuid(self):
        return UUID("66666666-7777-8888-9999-000000000000")

    @pytest.mark.asyncio
    async def test_get_by_id_returns_order(
        self, order_service, mock_order_repository, sample_uuid
    ):
        expected_order = Mock(spec=Order)
        mock_order_repository.get_by_id.return_value = expected_order

        result = await order_service.get_by_id(sample_uuid)

        assert result == expected_order
        mock_order_repository.get_by_id.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_get_all_returns_orders_list(
        self, order_service, mock_order_repository
    ):
        expected_orders = [Mock(spec=Order), Mock(spec=Order), Mock(spec=Order)]
        count = 15
        page = 1
        mock_order_repository.get_all.return_value = expected_orders

        result = await order_service.get_all(count=count, page=page)

        assert result == expected_orders
        mock_order_repository.get_all.assert_called_once_with(count, page)

    @pytest.mark.asyncio
    async def test_get_by_user_returns_orders_list(
        self, order_service, mock_order_repository, sample_uuid
    ):
        expected_orders = [Mock(spec=Order), Mock(spec=Order)]
        mock_order_repository.get_by_user.return_value = expected_orders

        result = await order_service.get_by_user(sample_uuid)

        assert result == expected_orders
        mock_order_repository.get_by_user.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_create_returns_new_order(self, order_service, mock_order_repository):
        order_data = Mock(spec=OrderCreate)
        expected_order = Mock(spec=Order)
        mock_order_repository.create.return_value = expected_order

        result = await order_service.create(order_data)

        assert result == expected_order
        mock_order_repository.create.assert_called_once_with(order_data)

    @pytest.mark.asyncio
    async def test_delete_calls_repository_delete(
        self, order_service, mock_order_repository, sample_uuid
    ):
        await order_service.delete(sample_uuid)

        mock_order_repository.delete.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_repository_methods_called_with_correct_arguments(
        self, order_service, mock_order_repository, sample_uuid, another_sample_uuid
    ):
        order_create_data = Mock(spec=OrderCreate)

        await order_service.get_by_id(sample_uuid)
        mock_order_repository.get_by_id.assert_called_with(sample_uuid)

        mock_order_repository.reset_mock()
        await order_service.get_all(count=10, page=3)
        mock_order_repository.get_all.assert_called_with(10, 3)

        mock_order_repository.reset_mock()
        await order_service.get_by_user(another_sample_uuid)
        mock_order_repository.get_by_user.assert_called_with(another_sample_uuid)

        mock_order_repository.reset_mock()
        await order_service.create(order_create_data)
        mock_order_repository.create.assert_called_with(order_create_data)

        mock_order_repository.reset_mock()
        await order_service.delete(sample_uuid)
        mock_order_repository.delete.assert_called_with(sample_uuid)
