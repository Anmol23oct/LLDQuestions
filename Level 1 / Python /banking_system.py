# banking_system.py

from account import Account
from transactions import DepositTransaction, TransferTransaction

class BankingSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account(account_id)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        transaction = DepositTransaction(timestamp, account_id, amount)
        return transaction.execute(self.accounts)

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> int | None:
        transaction = TransferTransaction(timestamp, source_id, target_id, amount)
        return transaction.execute(self.accounts)
