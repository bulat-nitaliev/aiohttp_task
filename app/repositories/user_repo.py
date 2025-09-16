from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import UserModel
from schemas.user import UserCreate
from typing import Optional
from dataclasses import dataclass


@dataclass
class UserRepository:
    session: AsyncSession

    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        # async with self.session() as session:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> UserModel:
        user = UserModel(username=user_data.username, email=user_data.email)
        user.set_password(user_data.password)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
