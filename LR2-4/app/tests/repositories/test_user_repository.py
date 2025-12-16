import pytest

from dto.user_dto import UserCreate, UserUpdate
from repositories.user_repository import UserRepository


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, user_repository: UserRepository):
        user_data = {
            "username": "Daniil",
            "email": "daniil@example.test",
            "description": "Developer"
        }

        user = await user_repository.create(UserCreate(**user_data))

        assert user.id is not None
        assert user.username == "Daniil"
        assert user.email == "daniil@example.test"
        assert user.description == "Developer"

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, user_repository: UserRepository):
        user = await user_repository.create(UserCreate(username="Ban", email="ban@example.com", description="Writer"))

        found_users = await user_repository.get_by_filter(1, 0, email="ban@example.com")
        found_user = found_users[0][0]

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == "ban@example.com"

    @pytest.mark.asyncio
    async def test_update_user(self, user_repository: UserRepository):
        user = await user_repository.create(UserCreate(username="John", email="john@example.com", description="Tester"))

        updated_user = await user_repository.update(user.id, UserUpdate(description="Updated description"))

        assert updated_user.username == "John"
        assert updated_user.email == "john@example.com"
        assert updated_user.description == "Updated description"

    @pytest.mark.asyncio
    async def test_delete_user(self, user_repository: UserRepository):
        user = await user_repository.create(UserCreate(username="Deleted", email="deleted@example.com", description="Tester"))

        await user_repository.delete(user.id)

        user = await user_repository.get_by_id(user.id)

        assert user is None

    @pytest.mark.asyncio
    async def test_get_users(self, user_repository: UserRepository):
        first = await user_repository.create(UserCreate(username="First", email="first@example.com", description="First"))
        second = await user_repository.create(UserCreate(username="Second", email="second@example.com", description="Second"))

        users = await user_repository.get_by_filter(2, 0)

        assert len(users[0]) == 2