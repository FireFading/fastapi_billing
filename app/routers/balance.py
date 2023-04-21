from app.config import jwt_settings
from app.database import get_session
from app.models.balance import Balance as ModelBalance
from app.models.balance import Transaction as ModelTransaction
from app.schemas.balance import Transaction
from app.utils.exceptions import get_user_or_404
from app.utils.messages import messages
from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/balance", tags=["balance"], responses={404: {"description": "Not found"}})
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.post("/topup/", status_code=status.HTTP_200_OK, summary="Accruing funds to the balance")
async def topup_balance(
    topup: Transaction,
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    if not (user_balance := await ModelBalance.get(session=session, user_id=user.guid)):
        user_balance = await ModelBalance(user_id=user.guid).create(session=session)
    await ModelTransaction(**topup.dict(), balance_id=user_balance.guid).add_money_to_balance(session=session)
    return {"balance": user_balance.deposit, "detail": messages.BALANCE_TOPUP}
