from app.config import jwt_settings
from fastapi import APIRouter
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

router = APIRouter(prefix="/balance", tags=["balance"], responses={404: {"description": "Not found"}})
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


# @router.post(
#     "/topup/", status_code=status.HTTP_200_OK, summary="Accruing funds to the balance"
# )
# async def topup_balance(
#     topup: Transaction,
#     credentials: HTTPAuthorizationCredentials = Security(security),
#     session: AsyncSession = Depends(get_session),
#     user: UserModel = Depends(get_user_or_404),
#     authorize: AuthJWT = Depends(),
# ):
#     authorize.jwt_required()
#     user_balance = await ModelBalance.get_or_create(session=session, user_id=user.guid)
#     await ModelTransaction(
#         **topup.dict(), balance_id=user_balance.guid
#     ).add_money_to_balance(session=session)
#     return {"balance": user_balance.deposit, "detail": messages.BALANCE_TOPUP}
