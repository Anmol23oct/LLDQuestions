# transactions.py

from abc import ABC, abstractmethod

class Transaction(ABC):
    def __init__(self, timestamp: int):
        self.timestamp = timestamp

    @abstractmethod
    def execute(self, accounts: dict):
        pass


class DepositTransaction(Transaction):
    def __init__(self, timestamp: int, account_id: str, amount: int):
        super().__init__(timestamp)
        self.account_id = account_id
        self.amount = amount

    def execute(self, accounts: dict) -> int | None:
        account = accounts.get(self.account_id)
        if not account:
            return None
        account.deposit(self.amount)
        return account.get_balance()


class TransferTransaction(Transaction):
    def __init__(self, timestamp: int, source_id: str, target_id: str, amount: int):
        super().__init__(timestamp)
        self.source_id = source_id
        self.target_id = target_id
        self.amount = amount

    def execute(self, accounts: dict) -> int | None:
        if self.source_id == self.target_id:
            return None

        source = accounts.get(self.source_id)
        target = accounts.get(self.target_id)

        if not source or not target or not source.can_withdraw(self.amount):
            return None

        source.withdraw(self.amount)
        target.deposit(self.amount)
        return source.get_balance()
