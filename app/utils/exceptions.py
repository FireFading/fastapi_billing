from app.models.users import User as UserModel
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_or_404(email: str, session: AsyncSession) -> UserModel | Exception:
    if not (user := await UserModel.get(session=session, email=email)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)
    return user
