from app.models.users import User as UserModel
from app.schemas.users import CreateUser
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class UserController:
    @classmethod
    async def create(cls, user_schema: CreateUser, session: AsyncSession):
        email = user_schema.email
        if await UserModel.get(session=session, email=email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.USER_ALREADY_EXISTS,
            )
        await UserModel(**user_schema.dict()).create(session=session)

    @classmethod
    async def get_or_404(cls, email: str, session: AsyncSession) -> UserModel | Exception:
        if not (user := await UserModel.get(session=session, email=email)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)
        return user


user_controller = UserController()
