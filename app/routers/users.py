from app.config import jwt_settings
from app.database import get_session
from app.models.users import User as UserModel
from app.schemas.users import CreateUser, LoginCredentials, UpdatePassword, User
from app.utils.exceptions import get_user_or_404
from app.utils.messages import messages
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/accounts", tags=["accounts"], responses={404: {"description": "Not found"}})
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Registration",
)
async def register(user: CreateUser, session: AsyncSession = Depends(get_session)):
    email = user.email
    if await UserModel.get(session=session, email=email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.USER_ALREADY_EXISTS)
    await UserModel(**user.dict()).create(session=session)
    return {"email": email, "detail": messages.USER_CREATED}


@router.post("/login/", status_code=status.HTTP_200_OK, summary="Authorization, get tokens")
async def login(
    login_credentials: LoginCredentials,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    user = await get_user_or_404(email=login_credentials.email, session=session)
    if not user.verify_password(password=login_credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.WRONG_PASSWORD)
    return {
        "access_token": authorize.create_access_token(subject=user.email),
        "refresh_token": authorize.create_refresh_token(subject=user.email),
    }


@router.delete("/logout/", status_code=status.HTTP_200_OK, summary="Logout")
async def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return {"detail": messages.USER_LOGOUT}


@router.post(
    "/change-password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Change password",
)
async def change_password(
    data: UpdatePassword,
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail=messages.PASSWORDS_NOT_MATCH,
        )
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    if user.verify_password(password=data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=messages.NEW_PASSWORD_SIMILAR_OLD,
        )
    await user.update(session=session)
    return {"detail": messages.PASSWORD_UPDATED}


@router.get("/info/", status_code=status.HTTP_200_OK, summary="User info")
async def get_user_info(
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    return User.from_orm(user)
