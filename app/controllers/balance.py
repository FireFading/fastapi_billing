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
    async def get_or_404(
        cls, user_id: uuid.UUID, session: AsyncSession
    ) -> BalanceModel | HTTPException:
        if not (
            user_balance := await BalanceModel.get(session=session, user_id=user_id)
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=messages.BALANCE_NOT_FOUND
            )
        return user_balance

    @staticmethod
    def check(deposit: float, amount: float) -> HTTPException | None:
        if deposit < abs(amount):
            print(deposit, amount)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=messages.INSUFFICIENT_FUNDS,
            )
        return None

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
        user: UserModel,
        transaction_schema: TransactionTopUp | TransactionWithdraw,
        session: AsyncSession,
        recipient_id: uuid.UUID | None = None,
        need_check: bool = False,
    ) -> float:
        transfer = bool(recipient_id)
        recipient_id = user.guid if recipient_id is None else recipient_id
        recipient_balance = await cls.get_or_404(user_id=recipient_id, session=session)
        if need_check:
            sender_balance = (
                await cls.get_or_404(user_id=user.guid, session=session)
                if recipient_id
                else recipient_balance
            )
            cls.check(deposit=sender_balance.deposit, amount=transaction_schema.amount)
        await TransactionModel(
            **transaction_schema.dict(), user=user, balance=recipient_balance
        ).create(
            session=session, transfer=transfer  # type: ignore
        )
        return recipient_balance.deposit


balance_controller = BalanceController()
