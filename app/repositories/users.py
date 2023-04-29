from app.models.users import User as UserModel
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=UserModel)

    async def create(self, instance: UserModel, session: AsyncSession):  # type: ignore
        instance.password = instance.get_hashed_password()
        return await super().create(instance=instance, session=session)

    async def update(self, instance, session: AsyncSession):
        instance.password = instance.get_hashed_password()
        return await super().update(instance=instance, session=session)


user_repository = UserRepository()
