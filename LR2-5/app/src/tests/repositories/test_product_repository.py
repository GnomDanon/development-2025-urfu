import pytest
from dto.produc_dto import ProductCreate, ProductUpdate
from repositories.product_repository import ProductRepository


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_create_product(self, product_repository: ProductRepository):
        product_data = {"name": "Apple", "price": 10, "count": 5}

        product = await product_repository.create(ProductCreate(**product_data))

        assert product.id is not None
        assert product.name == product_data["name"]
        assert product.price == product_data["price"]
        assert product.count == product_data["count"]

    @pytest.mark.asyncio
    async def test_update_product(self, product_repository: ProductRepository):
        product = await product_repository.create(
            ProductCreate(name="Apple", price=10, count=5)
        )

        updated_product = await product_repository.update(
            product.id, ProductUpdate(price=15)
        )

        assert updated_product.id is not None
        assert updated_product.name == "Apple"
        assert updated_product.price == 15
        assert updated_product.count == 5

    @pytest.mark.asyncio
    async def test_delete_product(self, product_repository: ProductRepository):
        product = await product_repository.create(
            ProductCreate(name="Apple", price=10, count=5)
        )

        await product_repository.delete(product.id)

        product = await product_repository.get_by_id(product.id)

        assert product is None

    @pytest.mark.asyncio
    async def test_get_products(self, product_repository: ProductRepository):
        first = await product_repository.create(
            ProductCreate(name="First", price=10, count=5)
        )
        second = await product_repository.create(
            ProductCreate(name="Second", price=20, count=10)
        )

        products = await product_repository.get_all(2, 0)

        assert len(products) == 2

    @pytest.mark.asyncio
    async def test_get_user_by_id(self, product_repository: ProductRepository):
        product = await product_repository.create(
            ProductCreate(name="Apple", price=10, count=5)
        )

        find_product = await product_repository.get_by_id(product.id)

        assert find_product is not None
        assert find_product.name == product.name
        assert find_product.price == product.price
