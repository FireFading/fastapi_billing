import uuid

from app.models.balance import Balance as BalanceModel
from app.models.balance import Transaction as TransactionModel
from app.models.users import User as UserModel
from app.schemas.transactions import TransactionTopUp, TransactionWithdraw
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class BalanceController:
    @classmethod
    async def get_or_404(cls, user_id: uuid.UUID, session: AsyncSession) -> BalanceModel | HTTPException:
        if not (user_balance := await BalanceModel.get(session=session, user_id=user_id)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.BALANCE_NOT_FOUND)
        return user_balance

    @classmethod
    async def get_and_check(cls, user_id, session: AsyncSession, amount: float) -> BalanceModel | HTTPException:
        user_balance = await cls.get_or_404(user_id=user_id, session=session)
        if user_balance.deposit < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.INSUFFICIENT_FUNDS,
            )
        return user_balance

    @classmethod
    async def create(cls, user: UserModel, session: AsyncSession):
        if user.balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.BALANCE_ALREADY_EXISTS,
            )
        await BalanceModel(user_id=user.guid).create(session=session)

    @classmethod
    async def update(
        cls,
        user_id,
        transaction_schema: TransactionTopUp | TransactionWithdraw,
        session: AsyncSession,
        need_check: bool = False,
    ) -> float:
        user_balance = (
            await cls.get_and_check(user_id=user_id, session=session, amount=transaction_schema.amount)
            if need_check
            else await cls.get_or_404(user_id=user_id, session=session)
        )
        await TransactionModel(**transaction_schema.dict(), user_id=user_id, balance=user_balance).create(
            session=session
        )
        return user_balance.deposit


balance_controller = BalanceController()
