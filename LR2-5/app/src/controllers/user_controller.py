from uuid import UUID

from dto.user_dto import UserCreate, UserListResponse, UserResponse, UserUpdate
from litestar import Controller, delete, get, post, put
from litestar.exceptions import NotFoundException
from litestar.params import Parameter
from services.user_service import UserService


class UserController(Controller):
    path = "/users"

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> UserResponse:
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"Пользователь с Id {user_id} не найден")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self,
        user_service: UserService,
        count: int = Parameter(default=10, gt=0),
        page: int = Parameter(default=0, ge=0),
    ) -> UserListResponse:
        users, total = await user_service.get_by_filter(count=count, page=page)
        return UserListResponse(
            users=[UserResponse.model_validate(user) for user in users], total=total
        )

    @post()
    async def create_user(
        self,
        user_service: UserService,
        data: UserCreate,
    ) -> UserResponse:
        user = await user_service.create(data)
        return UserResponse.model_validate(user)

    @delete("/{user_id:uuid}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: UUID,
    ) -> None:
        await user_service.delete(user_id)

    @put("/{user_id:uuid}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: UUID,
        data: UserUpdate,
    ) -> UserResponse:
        user = await user_service.update(user_id, data)
        return UserResponse.model_validate(user)
