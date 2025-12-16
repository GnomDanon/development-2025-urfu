from typing import List
from uuid import UUID

from dto.user_dto import UserCreate, UserUpdate
from entities import User
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_filter(
        self, count: int, page: int, **kwargs
    ) -> tuple[List[User], int]:
        count_stmt = select(func.count(User.id))
        for key, value in kwargs.items():
            if hasattr(User, key):
                count_stmt = count_stmt.where(getattr(User, key) == value)
        total = (await self.session.execute(count_stmt)).scalar_one()

        offset = count * page
        stmt = select(User)

        for key, value in kwargs.items():
            if hasattr(User, key):
                stmt = stmt.where(getattr(User, key) == value)

        stmt = stmt.offset(offset).limit(count)
        result = await self.session.execute(stmt)
        return list(result.scalars().all()), total

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError(f"User {user_id} not found")

        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            await self.session.delete(user)
            await self.session.commit()
