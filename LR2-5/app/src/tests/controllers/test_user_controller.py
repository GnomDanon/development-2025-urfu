from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
import pytest_asyncio
from controllers.user_controller import UserController
from dto.user_dto import UserCreate, UserListResponse, UserResponse, UserUpdate
from litestar.exceptions import NotFoundException
from services.user_service import UserService


class TestUserController:
    @pytest_asyncio.fixture
    def mock_user_service(self):
        return AsyncMock(spec=UserService)

    @pytest_asyncio.fixture
    def user_controller(self):
        return UserController()

    @pytest_asyncio.fixture
    def sample_uuid(self):
        return UUID("12345678-1234-5678-1234-567812345678")

    @pytest.mark.asyncio
    async def test_get_user_by_id_returns_user_response(
        self, user_controller, mock_user_service, sample_uuid
    ):
        mock_user = Mock()
        mock_user_service.get_by_id.return_value = mock_user
        expected_response = UserResponse.model_validate(mock_user)

        result = await user_controller.get_user_by_id(mock_user_service, sample_uuid)

        assert isinstance(result, UserResponse)
        mock_user_service.get_by_id.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_get_user_by_id_raises_not_found_exception_when_user_not_exists(
        self, user_controller, mock_user_service, sample_uuid
    ):
        mock_user_service.get_by_id.return_value = None

        with pytest.raises(
            NotFoundException, match=f"Пользователь с Id {sample_uuid} не найден"
        ):
            await user_controller.get_user_by_id(mock_user_service, sample_uuid)

    @pytest.mark.asyncio
    async def test_get_all_users_returns_user_list_response(
        self, user_controller, mock_user_service
    ):
        mock_users = [Mock(), Mock()]
        total_count = 2
        mock_user_service.get_by_filter.return_value = (mock_users, total_count)

        result = await user_controller.get_all_users(
            mock_user_service, count=10, page=0
        )

        assert isinstance(result, UserListResponse)
        assert len(result.users) == 2
        assert result.total == total_count
        mock_user_service.get_by_filter.assert_called_once_with(count=10, page=0)

    @pytest.mark.asyncio
    async def test_get_all_users_with_custom_pagination_params(
        self, user_controller, mock_user_service
    ):
        mock_users = [Mock()]
        total_count = 1
        mock_user_service.get_by_filter.return_value = (mock_users, total_count)

        result = await user_controller.get_all_users(mock_user_service, count=5, page=2)

        assert isinstance(result, UserListResponse)
        assert len(result.users) == 1
        assert result.total == 1
        mock_user_service.get_by_filter.assert_called_once_with(count=5, page=2)

    @pytest.mark.asyncio
    async def test_create_user_returns_user_response(
        self, user_controller, mock_user_service
    ):
        user_create_data = Mock(spec=UserCreate)
        mock_user = Mock()
        mock_user_service.create.return_value = mock_user
        expected_response = UserResponse.model_validate(mock_user)

        result = await user_controller.create_user(mock_user_service, user_create_data)

        assert isinstance(result, UserResponse)
        mock_user_service.create.assert_called_once_with(user_create_data)

    @pytest.mark.asyncio
    async def test_update_user_returns_user_response(
        self, user_controller, mock_user_service, sample_uuid
    ):
        user_update_data = Mock(spec=UserUpdate)
        mock_user = Mock()
        mock_user_service.update.return_value = mock_user
        expected_response = UserResponse.model_validate(mock_user)

        result = await user_controller.update_user(
            mock_user_service, sample_uuid, user_update_data
        )

        assert isinstance(result, UserResponse)
        mock_user_service.update.assert_called_once_with(sample_uuid, user_update_data)

    @pytest.mark.asyncio
    async def test_delete_user_calls_service_delete_method(
        self, user_controller, mock_user_service, sample_uuid
    ):
        await user_controller.delete_user(mock_user_service, sample_uuid)

        mock_user_service.delete.assert_called_once_with(sample_uuid)

    @pytest.mark.asyncio
    async def test_controller_path_is_correctly_set(self, user_controller):
        assert user_controller.path == "/users"

    @pytest.mark.asyncio
    async def test_controller_methods_call_correct_service_methods_with_parameters(
        self, user_controller, mock_user_service, sample_uuid
    ):
        mock_user = Mock()
        mock_user_service.get_by_id.return_value = mock_user
        await user_controller.get_user_by_id(mock_user_service, sample_uuid)
        mock_user_service.get_by_id.assert_called_with(sample_uuid)

        mock_user_service.reset_mock()
        mock_user_service.get_by_filter.return_value = ([Mock()], 1)
        await user_controller.get_all_users(mock_user_service, count=20, page=1)
        mock_user_service.get_by_filter.assert_called_with(count=20, page=1)

        mock_user_service.reset_mock()
        user_create_data = Mock(spec=UserCreate)
        mock_user_service.create.return_value = mock_user
        await user_controller.create_user(mock_user_service, user_create_data)
        mock_user_service.create.assert_called_with(user_create_data)

        mock_user_service.reset_mock()
        user_update_data = Mock(spec=UserUpdate)
        mock_user_service.update.return_value = mock_user
        await user_controller.update_user(
            mock_user_service, sample_uuid, user_update_data
        )
        mock_user_service.update.assert_called_with(sample_uuid, user_update_data)

        mock_user_service.reset_mock()
        await user_controller.delete_user(mock_user_service, sample_uuid)
        mock_user_service.delete.assert_called_with(sample_uuid)
