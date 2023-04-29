import uuid

from app.models.balance import Balance as BalanceModel
from app.models.balance import Transaction as TransactionModel
from app.models.users import User as UserModel
from app.repositories.balance import balance_repository, transaction_repository
from app.schemas.balance import CreateBalance
from app.schemas.transactions import TransactionTopUp, TransactionWithdraw
from app.utils.messages import messages
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import CurrencyType


class BalanceController:
    @classmethod
    async def get_or_404(
        cls,
        user_id: uuid.UUID,
        session: AsyncSession,
        currency: CurrencyType = "USD",
    ) -> BalanceModel | HTTPException:
        if not (
            user_balance := await balance_repository.get(  # type: ignore
                session=session, user_id=user_id, currency=currency
            )
        ):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.BALANCE_NOT_FOUND)
        return user_balance

    @staticmethod
    def check(deposit: float, amount: float) -> HTTPException | None:
        if deposit < abs(amount):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.INSUFFICIENT_FUNDS,
            )
        return None

    @classmethod
    async def create(cls, user: UserModel, balance_schema: CreateBalance, session: AsyncSession):
        if await balance_repository.get(
            user_id=user.guid, session=session, currency=balance_schema.currency
        ):  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.BALANCE_ALREADY_EXISTS,
            )
        balance = BalanceModel(user_id=user.guid, currency=balance_schema.currency)
        await balance_repository.create(instance=balance, session=session)

    @classmethod
    async def update(
        cls,
        user: UserModel,
        transaction_schema: TransactionTopUp | TransactionWithdraw,
        session: AsyncSession,
        recipient_id: uuid.UUID | None = None,
        need_check: bool = False,
    ) -> float:
        transfer = bool(recipient_id)
        recipient_id = recipient_id or user.guid
        recipient_balance = await cls.get_or_404(
            user_id=recipient_id, currency=transaction_schema.currency, session=session
        )
        if need_check:
            sender_balance = (
                await cls.get_or_404(
                    user_id=user.guid,
                    currency=transaction_schema.currency,
                    session=session,
                )
                if transfer
                else recipient_balance
            )
            cls.check(deposit=sender_balance.deposit, amount=transaction_schema.amount)
        transaction = TransactionModel(**transaction_schema.dict(), user=user, balance=recipient_balance)
        if transfer:
            await balance_repository.update(
                balance=sender_balance,
                transaction_amount=transaction_schema.amount,
                session=session,
            )
        await balance_repository.update(
            balance=recipient_balance,
            transaction_amount=transaction_schema.amount,
            session=session,
        )
        await transaction_repository.create(instance=transaction, session=session)
        return recipient_balance.deposit


balance_controller = BalanceController()
