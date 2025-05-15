from typing import Dict, List, Optional

# 📦 Transaction Record
class Transaction:
    def __init__(self, timestamp: int, type: str, amount: int, target_account: Optional[str] = None):
        self.timestamp = timestamp
        self.type = type  # deposit, withdraw, transfer_out, transfer_in
        self.amount = amount
        self.target_account = target_account

    def __repr__(self):
        if self.type.startswith("transfer"):
            return f"{self.timestamp}: {self.type} {self.amount} to/from {self.target_account}"
        return f"{self.timestamp}: {self.type} {self.amount}"

# 🧾 BankAccount class
class BankAccount:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.transactions: List[Transaction] = []
        self.total_outgoing = 0  # 🔥 Track total outgoing

    def deposit(self, timestamp: int, amount: int) -> int:
        self.balance += amount
        self.transactions.append(Transaction(timestamp, "deposit", amount))
        return self.balance

    def can_withdraw(self, amount: int) -> bool:
        return self.balance >= amount

    def withdraw(self, timestamp: int, amount: int) -> int:
        if self.can_withdraw(amount):
            self.balance -= amount
            self.total_outgoing += amount
            self.transactions.append(Transaction(timestamp, "withdraw", amount))
            return self.balance
        else:
            raise ValueError("Insufficient funds")

    def transfer_out(self, timestamp: int, amount: int, target_account: str):
        self.balance -= amount
        self.total_outgoing += amount
        self.transactions.append(Transaction(timestamp, "transfer_out", amount, target_account))

    def transfer_in(self, timestamp: int, amount: int, source_account: str):
        self.balance += amount
        self.transactions.append(Transaction(timestamp, "transfer_in", amount, source_account))

    def get_transaction_history(self) -> List[Transaction]:
        return self.transactions

# 🗃️ Account Repository
class InMemoryAccountRepository:
    def __init__(self):
        self._accounts: Dict[str, BankAccount] = {}

    def create_account(self, account_id: str) -> bool:
        if account_id in self._accounts:
            return False
        self._accounts[account_id] = BankAccount(account_id)
        return True

    def get_account(self, account_id: str) -> Optional[BankAccount]:
        return self._accounts.get(account_id)

    def get_all_accounts(self) -> List[BankAccount]:
        return list(self._accounts.values())

# 🧠 Bank Service
class BankService:
    def __init__(self):
        self.repo = InMemoryAccountRepository()

    def create_account(self, timestamp: int, account_id: str) -> bool:
        return self.repo.create_account(account_id)

    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        account = self.repo.get_account(account_id)
        if not account:
            return None
        return account.deposit(timestamp, amount)

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> Optional[int]:
        if source_id == target_id:
            return None
        source = self.repo.get_account(source_id)
        target = self.repo.get_account(target_id)
        if not source or not target or not source.can_withdraw(amount):
            return None
        source.transfer_out(timestamp, amount, target_id)
        target.transfer_in(timestamp, amount, source_id)
        return source.balance

    def get_transaction_history(self, account_id: str) -> Optional[List[Transaction]]:
        account = self.repo.get_account(account_id)
        if not account:
            return None
        return account.get_transaction_history()

    def top_spenders(self, timestamp: int, n: int) -> List[str]:
        accounts = self.repo.get_all_accounts()

        # Sort by total_outgoing DESC, then account_id ASC
        sorted_accounts = sorted(
            accounts,
            key=lambda acc: (-acc.total_outgoing, acc.account_id)
        )

        return [f"{acc.account_id}({acc.total_outgoing})" for acc in sorted_accounts[:n]]
