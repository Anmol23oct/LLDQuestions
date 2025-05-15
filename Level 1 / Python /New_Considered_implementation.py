from typing import Dict, Optional

# 📦 Entity
class BankAccount:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0

    def deposit(self, amount: int) -> int:
        self.balance += amount
        return self.balance

    def can_withdraw(self, amount: int) -> bool:
        return self.balance >= amount

    def withdraw(self, amount: int) -> int:
        if self.can_withdraw(amount):
            self.balance -= amount
            return self.balance
        else:
            raise ValueError("Insufficient funds")

# 📚 Repository Interface
class IAccountRepository:
    def create_account(self, account_id: str) -> bool:
        raise NotImplementedError

    def get_account(self, account_id: str) -> Optional[BankAccount]:
        raise NotImplementedError

# 💾 In-memory Repository
class InMemoryAccountRepository(IAccountRepository):
    def __init__(self):
        self._accounts: Dict[str, BankAccount] = {}

    def create_account(self, account_id: str) -> bool:
        if account_id in self._accounts:
            return False
        self._accounts[account_id] = BankAccount(account_id)
        return True

    def get_account(self, account_id: str) -> Optional[BankAccount]:
        return self._accounts.get(account_id)

# 🧠 Business Logic Layer (Service)
class BankService:
    def __init__(self, account_repository: IAccountRepository):
        self.account_repository = account_repository

    def create_account(self, timestamp: int, account_id: str) -> bool:
        return self.account_repository.create_account(account_id)

    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        account = self.account_repository.get_account(account_id)
        if not account:
            return None
        return account.deposit(amount)

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> Optional[int]:
        if source_account_id == target_account_id:
            return None

        source = self.account_repository.get_account(source_account_id)
        target = self.account_repository.get_account(target_account_id)

        if not source or not target:
            return None
        if not source.can_withdraw(amount):
            return None

        source.withdraw(amount)
        target.deposit(amount)
        return source.balance
