from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
import pytest_asyncio
from dto.user_dto import UserCreate, UserUpdate
from entities import User
from repositories.user_repository import UserRepository
from services.user_service import UserService


class TestUserService:
    @pytest_asyncio.fixture
    def mock_user_repository(self):
        return AsyncMock(spec=UserRepository)

    @pytest_asyncio.fixture
    def user_service(self, mock_user_repository):
        return UserService(user_repository=mock_user_repository)

    @pytest_asyncio.fixture
    def sample_uuid(self):
        return UUID("12345678-1234-5678-1234-567812345678")

    @pytest.mark.asyncio
    async def test_get_by_id_returns_user(
        self, user_service, mock_user_repository, sample_uuid
    ):
        expected_user = Mock(spec=User)
        mock_user_repository.get_by_id.return_value = expected_user

        result = await user_service.get_by_id(sample_uuid)

        assert result == expected_user
        mock_user_repository.get_by_id.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_get_by_id_returns_none_when_user_not_found(
        self, user_service, mock_user_repository, sample_uuid
    ):
        mock_user_repository.get_by_id.return_value = None

        result = await user_service.get_by_id(sample_uuid)

        assert result is None
        mock_user_repository.get_by_id.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_get_by_filter_returns_users_and_count(
        self, user_service, mock_user_repository
    ):
        expected_users = [Mock(spec=User), Mock(spec=User)]
        expected_total_count = 2
        count = 10
        page = 1
        filter_kwargs = {"name": "test", "email": "test@example.com"}

        mock_user_repository.get_by_filter.return_value = (
            expected_users,
            expected_total_count,
        )

        result_users, result_count = await user_service.get_by_filter(
            count=count, page=page, **filter_kwargs
        )

        assert result_users == expected_users
        assert result_count == expected_total_count
        mock_user_repository.get_by_filter.assert_called_once_with(
            count=count, page=page, **filter_kwargs
        )

    @pytest.mark.asyncio
    async def test_create_returns_new_user(self, user_service, mock_user_repository):
        user_data = Mock(spec=UserCreate)
        expected_user = Mock(spec=User)
        mock_user_repository.create.return_value = expected_user

        result = await user_service.create(user_data)

        assert result == expected_user
        mock_user_repository.create.assert_called_once_with(user_data)

    @pytest.mark.asyncio
    async def test_update_returns_updated_user(
        self, user_service, mock_user_repository, sample_uuid
    ):
        user_data = Mock(spec=UserUpdate)
        expected_user = Mock(spec=User)
        mock_user_repository.update.return_value = expected_user

        result = await user_service.update(sample_uuid, user_data)

        assert result == expected_user
        mock_user_repository.update.assert_called_once_with(sample_uuid, user_data)

    @pytest.mark.asyncio
    async def test_delete_calls_repository_delete(
        self, user_service, mock_user_repository, sample_uuid
    ):
        await user_service.delete(sample_uuid)

        mock_user_repository.delete.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_repository_methods_called_with_correct_arguments(
        self, user_service, mock_user_repository, sample_uuid
    ):
        user_create_data = Mock(spec=UserCreate)
        user_update_data = Mock(spec=UserUpdate)

        await user_service.get_by_id(sample_uuid)
        mock_user_repository.get_by_id.assert_called_with(sample_uuid)

        mock_user_repository.reset_mock()
        await user_service.get_by_filter(count=5, page=1, status="active")
        mock_user_repository.get_by_filter.assert_called_with(
            count=5, page=1, status="active"
        )

        await user_service.create(user_create_data)
        mock_user_repository.create.assert_called_with(user_create_data)

        await user_service.update(sample_uuid, user_update_data)
        mock_user_repository.update.assert_called_with(sample_uuid, user_update_data)

        await user_service.delete(sample_uuid)
        mock_user_repository.delete.assert_called_with(sample_uuid)
