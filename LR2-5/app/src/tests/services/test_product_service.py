from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
import pytest_asyncio
from dto.produc_dto import ProductCreate, ProductUpdate
from entities import Product
from repositories.product_repository import ProductRepository
from services.product_service import ProductService


class TestProductService:
    @pytest_asyncio.fixture
    def mock_product_repository(self):
        return AsyncMock(spec=ProductRepository)

    @pytest_asyncio.fixture
    def product_service(self, mock_product_repository):
        return ProductService(product_repository=mock_product_repository)

    @pytest_asyncio.fixture
    def sample_uuid(self):
        return UUID("87654321-4321-8765-4321-876543210987")

    @pytest.mark.asyncio
    async def test_get_by_id_returns_product(
        self, product_service, mock_product_repository, sample_uuid
    ):
        expected_product = Mock(spec=Product)
        mock_product_repository.get_by_id.return_value = expected_product

        result = await product_service.get_by_id(sample_uuid)

        assert result == expected_product
        mock_product_repository.get_by_id.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_get_all_returns_products_list(
        self, product_service, mock_product_repository
    ):
        expected_products = [Mock(spec=Product), Mock(spec=Product)]
        count = 10
        page = 1
        mock_product_repository.get_all.return_value = expected_products

        result = await product_service.get_all(count=count, page=page)

        assert result == expected_products
        mock_product_repository.get_all.assert_called_once_with(count, page)

    @pytest.mark.asyncio
    async def test_create_returns_new_product(
        self, product_service, mock_product_repository
    ):
        product_data = Mock(spec=ProductCreate)
        expected_product = Mock(spec=Product)
        mock_product_repository.create.return_value = expected_product

        result = await product_service.create(product_data)

        assert result == expected_product
        mock_product_repository.create.assert_called_once_with(product_data)

    @pytest.mark.asyncio
    async def test_update_returns_updated_product(
        self, product_service, mock_product_repository, sample_uuid
    ):
        product_data = Mock(spec=ProductUpdate)
        expected_product = Mock(spec=Product)
        mock_product_repository.update.return_value = expected_product

        result = await product_service.update(sample_uuid, product_data)

        assert result == expected_product
        mock_product_repository.update.assert_called_once_with(
            sample_uuid, product_data
        )

    @pytest.mark.asyncio
    async def test_delete_calls_repository_delete(
        self, product_service, mock_product_repository, sample_uuid
    ):
        await product_service.delete(sample_uuid)

        mock_product_repository.delete.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_repository_methods_called_with_correct_arguments(
        self, product_service, mock_product_repository, sample_uuid
    ):
        product_create_data = Mock(spec=ProductCreate)
        product_update_data = Mock(spec=ProductUpdate)

        await product_service.get_by_id(sample_uuid)
        mock_product_repository.get_by_id.assert_called_with(sample_uuid)

        mock_product_repository.reset_mock()
        await product_service.get_all(count=5, page=2)
        mock_product_repository.get_all.assert_called_with(5, 2)

        await product_service.create(product_create_data)
        mock_product_repository.create.assert_called_with(product_create_data)

        await product_service.update(sample_uuid, product_update_data)
        mock_product_repository.update.assert_called_with(
            sample_uuid, product_update_data
        )

        await product_service.delete(sample_uuid)
        mock_product_repository.delete.assert_called_with(sample_uuid)
