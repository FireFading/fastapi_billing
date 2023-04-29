from datetime import datetime, timedelta

import jwt
from app.config import settings
from app.models.users import User as UserModel
from app.repositories.users import user_repository
from app.schemas.users import CreateUser, UpdatePassword
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class UserController:
    @classmethod
    async def create(cls, user_schema: CreateUser, session: AsyncSession) -> UserModel | Exception:
        email = user_schema.email
        if await user_repository.get(session=session, email=email):  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.USER_ALREADY_EXISTS,
            )
        user = UserModel(**user_schema.dict())
        return await user_repository.create(instance=user, session=session)

    @classmethod
    async def get_or_404(cls, email: str, session: AsyncSession) -> UserModel | Exception:
        if not (user := await user_repository.get(session=session, email=email)):  # type: ignore
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)
        return user

    @classmethod
    async def update_password(cls, email: str, change_password_schema: UpdatePassword, session: AsyncSession):
        user = await cls.get_or_404(email=email, session=session)
        if not user.verify_password(password=change_password_schema.old_password):
            raise HTTPException(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                detail=messages.WRONG_OLD_PASSWORD,
            )
        if user.verify_password(password=change_password_schema.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.NEW_PASSWORD_SIMILAR_OLD,
            )
        await user_repository.update(instance=user, session=session)

    @classmethod
    async def reset_password(cls, token: str, new_password: str, session: AsyncSession):
        if not cls.verify_token(token=token):
            raise HTTPException(
                status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
                detail=messages.INVALID_TOKEN,
            )
        email = cls.get_email_from_token(token=token)
        user = await cls.get_or_404(email=email, session=session)
        user.password = user.get_hashed_password()
        await user_repository.update(instance=user, session=session)

    @staticmethod
    def verify_token(token: str) -> bool:
        try:
            token_data = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
        except Exception:
            return False
        expires_in = token_data.get("exp")
        is_active = token_data.get("is_active")
        return bool(datetime.now().timestamp() < expires_in and is_active)

    @staticmethod
    def create_token(email: str) -> str:
        expires_in = (datetime.now() + timedelta(hours=settings.token_expires_hours)).timestamp()
        payload = {"exp": expires_in, "email": email, "is_active": True}
        return jwt.encode(payload=payload, key=settings.secret_key, algorithm=settings.algorithm).decode("utf-8")

    @staticmethod
    def get_email_from_token(token: str) -> str:
        token_data = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
        return token_data.get("email")


user_controller = UserController()
