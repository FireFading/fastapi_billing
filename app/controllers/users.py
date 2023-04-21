from datetime import datetime, timedelta

import jwt
from app.config import settings
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
