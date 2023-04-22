from app.config import jwt_settings
from app.controllers.balance import balance_controller
from app.controllers.users import user_controller
from app.database import get_session
from app.schemas.transactions import (
    ShowTransaction,
    TransactionTopUp,
    TransactionWithdraw,
)
from app.schemas.balance import CreateBalance
from app.utils.messages import messages
from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/balance", tags=["balance"], responses={404: {"description": "Not found"}}
)
security = HTTPBearer()


@AuthJWT.load_config
def get_jwt_settings():
    return jwt_settings


@router.post("/create/", status_code=status.HTTP_201_CREATED, summary="Create balance")
async def create_balance(
    balance_schema: CreateBalance = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    print(balance_schema)
    authorize.jwt_required()
    user = await user_controller.get_or_404(
        email=authorize.get_jwt_subject(), session=session
    )
    await balance_controller.create(user=user, balance_schema=balance_schema, session=session)  # type: ignore
    return {"detail": messages.BALANCE_CREATED}


@router.post(
    "/top-up/",
    status_code=status.HTTP_200_OK,
    summary="Accruing funds to the own balance",
)
async def top_up_balance(
    top_up_schema: TransactionTopUp,
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    user = await user_controller.get_or_404(
        email=authorize.get_jwt_subject(), session=session
    )
    deposit = await balance_controller.update(
        user=user,  # type: ignore
        session=session,
        transaction_schema=top_up_schema,
    )
    return {"deposit": deposit, "detail": messages.BALANCE_TOP_UP}


@router.get(
    "/deposit/", status_code=status.HTTP_200_OK, summary="Get amount of deposit balance"
)
async def get_deposit_amount(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await user_controller.get_or_404(email=email, session=session)
    user_balance = await balance_controller.get_or_404(
        user_id=user.guid, session=session
    )
    return {"deposit": user_balance.deposit}


@router.post(
    "/withdraw/",
    status_code=status.HTTP_200_OK,
    summary="Withdrawing funds from the own balance",
)
async def withdraw_balance(
    withdraw_schema: TransactionWithdraw,
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await user_controller.get_or_404(email=email, session=session)
    deposit = await balance_controller.update(
        user=user,  # type: ignore
        session=session,
        transaction_schema=withdraw_schema,
        need_check=True,
    )
    return {"deposit": deposit, "detail": messages.BALANCE_WITHDRAW}


@router.get(
    "/history/", status_code=status.HTTP_200_OK, summary="Get history of transactions"
)
async def get_balance_history(
    balance_schema: CreateBalance = Depends(),
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(get_session),
    authorize: AuthJWT = Depends(),
):
    authorize.jwt_required()
    email = authorize.get_jwt_subject()
    user = await user_controller.get_or_404(email=email, session=session)
    user_balance = await balance_controller.get_or_404(
        user_id=user.guid, currency=balance_schema.currency, session=session
    )
    return (
        [
            ShowTransaction.from_orm(transaction)
            for transaction in user_balance.transactions
        ]
        if user_balance.transactions
        else None
    )
