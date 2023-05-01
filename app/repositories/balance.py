from app.models.balance import Balance as BalanceModel
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class BalanceRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=BalanceModel)

    async def downgrade(self, balance: BalanceModel, transaction_amount: float, session: AsyncSession):
        balance.deposit -= transaction_amount
        return await super().update(instance=balance, session=session)

    async def upgrade(self, balance: BalanceModel, transaction_amount: float, session: AsyncSession):
        balance.deposit += transaction_amount
        return await super().update(instance=balance, session=session)


balance_repository = BalanceRepository()
