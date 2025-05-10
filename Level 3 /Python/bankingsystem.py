from account import Account
from transactions import DepositTransaction, TransferTransaction
import heapq

class BankingSystem:
    def __init__(self):
        self.accounts = {}  # account_id -> Account
        self.outgoing_totals = {}  # account_id -> int
        self.payment_counter = 0  # to generate payment IDs
        self.scheduled_cashbacks = []  # min-heap of (timestamp, account_id, amount, payment_id)
        self.payment_status = {}  # account_id -> {payment_id: "IN_PROGRESS"/"CASHBACK_RECEIVED"}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account(account_id)
        self.outgoing_totals[account_id] = 0
        self.payment_status[account_id] = {}
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._process_cashbacks(timestamp)

        transaction = DepositTransaction(timestamp, account_id, amount)
        return transaction.execute(self.accounts)

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> int | None:
        self._process_cashbacks(timestamp)

        transaction = TransferTransaction(timestamp, source_id, target_id, amount)
        result = transaction.execute(self.accounts)
        if result is not None:
            self.outgoing_totals[source_id] += amount
        return result

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        self._process_cashbacks(timestamp)

        if account_id not in self.accounts:
            return None
        account = self.accounts[account_id]
        if not account.can_withdraw(amount):
            return None

        account.withdraw(amount)
        self.outgoing_totals[account_id] += amount

        self.payment_counter += 1
        payment_id = f"payment{self.payment_counter}"
        cashback_amount = amount * 2 // 100

        cashback_time = timestamp + MILLISECONDS_IN_1_DAY
        heapq.heappush(self.scheduled_cashbacks, (cashback_time, account_id, cashback_amount, payment_id))

        self.payment_status[account_id][payment_id] = "IN_PROGRESS"
        return payment_id

    def get_payment_status(self, timestamp: int, account_id: str, payment_id: str) -> str | None:
        self._process_cashbacks(timestamp)

        if account_id not in self.accounts:
            return None
        status_map = self.payment_status.get(account_id, {})
        if payment_id not in status_map:
            return None
        return status_map[payment_id]

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        self._process_cashbacks(timestamp)

        sorted_accounts = sorted(
            self.outgoing_totals.items(),
            key=lambda item: (-item[1], item[0])
        )
        return [f"{acc_id}({total})" for acc_id, total in sorted_accounts[:n]]

    def _process_cashbacks(self, current_timestamp: int):
        while self.scheduled_cashbacks and self.scheduled_cashbacks[0][0] <= current_timestamp:
            _, account_id, cashback_amount, payment_id = heapq.heappop(self.scheduled_cashbacks)
            if account_id in self.accounts:
                self.accounts[account_id].deposit(cashback_amount)
                self.payment_status[account_id][payment_id] = "CASHBACK_RECEIVED"



if __name__ == "__main__":
    bank = BankingSystem()
    MILLISECONDS_IN_1_DAY = 86400000

    bank.create_account(1, "account1")
    bank.create_account(2, "account2")

    bank.deposit(3, "account1", 2000)

    print(bank.pay(4, "account1", 1000))  # payment1
    print(bank.pay(100, "account1", 1000))  # payment2

    print(bank.get_payment_status(101, "non-existing", "payment1"))  # None
    print(bank.get_payment_status(102, "account2", "payment1"))  # None
    print(bank.get_payment_status(103, "account1", "payment1"))  # IN_PROGRESS
    print(bank.top_spenders(104, 2))  # ['account1(2000)', 'account2(0)']

    print(bank.deposit(4 + MILLISECONDS_IN_1_DAY, "account1", 100))  # cashback applied + deposit
    print(bank.get_payment_status(4 + MILLISECONDS_IN_1_DAY, "account1", "payment1"))  # CASHBACK_RECEIVED
