from app.config import jwt_settings
from app.database import get_session
from app.models.balance import Balance as ModelBalance
from app.models.balance import Transaction as ModelTransaction
from app.schemas.transactions import ShowTransaction, TransactionTopUp, TransactionWithdraw
from app.utils.exceptions import get_user_or_404
from app.utils.messages import messages
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/balance", tags=["balance"], responses={404: {"description": "Not found"}})
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.post(
    "/top-up/",
    status_code=status.HTTP_200_OK,
    summary="Accruing funds to the own balance",
)
async def top_up_balance(
    top_up: TransactionTopUp,
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    if not (user_balance := await ModelBalance.get(session=session, user_id=user.guid)):
        user_balance = await ModelBalance(user_id=user.guid).create(session=session)
    await ModelTransaction(**top_up.dict(), user_id=user.guid, balance=user_balance).create(session=session)
    return {"deposit": user_balance.deposit, "detail": messages.BALANCE_TOP_UP}


@router.get("/deposit/", status_code=status.HTTP_200_OK, summary="Get amount of deposit balance")
async def get_deposit_amount(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    if not (user_balance := await ModelBalance.get(session=session, user_id=user.guid)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.BALANCE_NOT_FOUND)
    return {"deposit": user_balance.deposit}


@router.post(
    "/withdraw/",
    status_code=status.HTTP_200_OK,
    summary="Withdrawing funds from the own balance",
)
async def withdraw_balance(
    withdraw: TransactionWithdraw,
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    if not (user_balance := await ModelBalance.get(session=session, user_id=user.guid)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.BALANCE_NOT_FOUND)
    if user_balance.deposit < withdraw.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=messages.INSUFFICIENT_FUNDS)
    await ModelTransaction(**withdraw.dict(), user_id=user.guid, balance=user_balance).create(session=session)
    return {"deposit": user_balance.deposit, "detail": messages.BALANCE_WITHDRAW}


@router.get("/history/", status_code=status.HTTP_200_OK, summary="Get history of transactions")
async def get_balance_history(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await get_user_or_404(email=email, session=session)
    if not user.balance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.BALANCE_NOT_FOUND)
    return (
        [ShowTransaction.from_orm(transaction) for transaction in user.balance.transactions]
        if user.balance.transactions
        else None
    )
