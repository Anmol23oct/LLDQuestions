from account import Account
from transactions import DepositTransaction, TransferTransaction

class BankingSystem:
    def __init__(self):
        self.accounts = {}  # account_id -> Account
        self.outgoing_totals = {}  # account_id -> total outgoing

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account(account_id)
        self.outgoing_totals[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        transaction = DepositTransaction(timestamp, account_id, amount)
        return transaction.execute(self.accounts)

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> int | None:
        transaction = TransferTransaction(timestamp, source_id, target_id, amount)
        result = transaction.execute(self.accounts)

        if result is not None:
            self.outgoing_totals[source_id] += amount

        return result

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        # Sort by total outgoing desc, then account_id asc
        sorted_accounts = sorted(
            self.outgoing_totals.items(),
            key=lambda item: (-item[1], item[0])
        )
        return [f"{acc_id}({total})" for acc_id, total in sorted_accounts[:n]]
