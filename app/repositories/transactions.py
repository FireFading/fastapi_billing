from app.models.transactions import Transaction as TransactionModel
from app.repositories.base import BaseRepository


class TransactionRepository(BaseRepository):
    def __init__(self):
        super().__init__(model=TransactionModel)


transaction_repository = TransactionRepository()
