from typing import Dict, List, Optional
import heapq

MILLISECONDS_IN_1_DAY = 86400000

# ✅ New class: for storing payment metadata and status
class Payment:
    def __init__(self, id: str, account_id: str, amount: int, pay_ts: int):
        self.id = id
        self.account_id = account_id
        self.amount = amount
        self.status = "IN_PROGRESS"
        self.pay_timestamp = pay_ts
        self.cashback_ts = pay_ts + MILLISECONDS_IN_1_DAY  # cashback trigger time
        self.cashback_amount = amount // 50  # 2% cashback

# ✅ Transaction remains the same
class Transaction:
    def __init__(self, timestamp: int, type: str, amount: int, target_account: Optional[str] = None):
        self.timestamp = timestamp
        self.type = type
        self.amount = amount
        self.target_account = target_account

    def __repr__(self):
        if self.target_account:
            return f"{self.timestamp}: {self.type} {self.amount} to/from {self.target_account}"
        return f"{self.timestamp}: {self.type} {self.amount}"

# ✅ Extended BankAccount to track payments and process cashback
class BankAccount:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.transactions: List[Transaction] = []
        self.total_outgoing = 0
        self.payments: Dict[str, Payment] = {}  # 🔸 added to track payments

    def deposit(self, timestamp: int, amount: int):
        self.balance += amount
        self.transactions.append(Transaction(timestamp, "deposit", amount))
        return self.balance

    def can_withdraw(self, amount: int):
        return self.balance >= amount

    def withdraw(self, timestamp: int, amount: int):
        self.balance -= amount
        self.total_outgoing += amount  # 🔸 added to count toward top spenders
        self.transactions.append(Transaction(timestamp, "withdraw", amount))

    def transfer_out(self, timestamp: int, amount: int, target_account: str):
        self.balance -= amount
        self.total_outgoing += amount
        self.transactions.append(Transaction(timestamp, "transfer_out", amount, target_account))

    def transfer_in(self, timestamp: int, amount: int, source_account: str):
        self.balance += amount
        self.transactions.append(Transaction(timestamp, "transfer_in", amount, source_account))

    # ✅ New: pay operation (includes cashback scheduling)
    def pay(self, timestamp: int, amount: int, payment_id: str):
        self.balance -= amount
        self.total_outgoing += amount
        self.transactions.append(Transaction(timestamp, "pay", amount))
        payment = Payment(payment_id, self.account_id, amount, timestamp)
        self.payments[payment_id] = payment
        return payment

    # ✅ New: process a single cashback for a payment at timestamp
    def process_cashback(self, timestamp: int, payment_id: str):
        payment = self.payments[payment_id]
        if payment.status == "IN_PROGRESS" and timestamp >= payment.cashback_ts:
            self.balance += payment.cashback_amount
            payment.status = "CASHBACK_RECEIVED"
            self.transactions.append(Transaction(timestamp, "cashback", payment.cashback_amount))

    def get_transaction_history(self):
        return self.transactions

# ✅ Unchanged except for get_all_accounts()
class InMemoryAccountRepository:
    def __init__(self):
        self.accounts: Dict[str, BankAccount] = {}

    def create_account(self, account_id: str):
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = BankAccount(account_id)
        return True

    def get_account(self, account_id: str):
        return self.accounts.get(account_id)

    def get_all_accounts(self):
        return list(self.accounts.values())  # 🔸 used in top_spenders

# ✅ BankService: the orchestrator with cashback scheduling
class BankService:
    def __init__(self):
        self.repo = InMemoryAccountRepository()
        self.payment_counter = 1  # 🔸 for payment ids like payment1, payment2
        self.cashback_schedule = []  # 🔸 min-heap: (timestamp, account_id, payment_id)

    # ✅ New internal helper to process pending cashback before timestamp
    def _process_due_cashbacks(self, timestamp: int):
        while self.cashback_schedule and self.cashback_schedule[0][0] <= timestamp:
            ts, account_id, payment_id = heapq.heappop(self.cashback_schedule)
            account = self.repo.get_account(account_id)
            if account and payment_id in account.payments:
                account.process_cashback(ts, payment_id)

    def create_account(self, timestamp: int, account_id: str):
        self._process_due_cashbacks(timestamp)  # 🔸 process any cashback first
        return self.repo.create_account(account_id)

    def deposit(self, timestamp: int, account_id: str, amount: int):
        self._process_due_cashbacks(timestamp)
        account = self.repo.get_account(account_id)
        if not account:
            return None
        return account.deposit(timestamp, amount)

    def transfer(self, timestamp: int, source: str, target: str, amount: int):
        self._process_due_cashbacks(timestamp)
        if source == target:
            return None
        src_acc = self.repo.get_account(source)
        tgt_acc = self.repo.get_account(target)
        if not src_acc or not tgt_acc or not src_acc.can_withdraw(amount):
            return None
        src_acc.transfer_out(timestamp, amount, target)
        tgt_acc.transfer_in(timestamp, amount, source)
        return src_acc.balance

    # ✅ New: schedule a payment with cashback
    def pay(self, timestamp: int, account_id: str, amount: int) -> Optional[str]:
        self._process_due_cashbacks(timestamp)
        account = self.repo.get_account(account_id)
        if not account or not account.can_withdraw(amount):
            return None
        payment_id = f"payment{self.payment_counter}"
        self.payment_counter += 1
        payment = account.pay(timestamp, amount, payment_id)
        heapq.heappush(self.cashback_schedule, (payment.cashback_ts, account_id, payment_id))  # 🔸 schedule cashback
        return payment_id

    # ✅ New: check payment status
    def get_payment_status(self, timestamp: int, account_id: str, payment_id: str):
        self._process_due_cashbacks(timestamp)
        account = self.repo.get_account(account_id)
        if not account:
            return None
        payment = account.payments.get(payment_id)
        if not payment or payment.account_id != account_id:
            return None
        return payment.status

    # ✅ Updated: now includes pay + transfer_out + withdraw
    def top_spenders(self, timestamp: int, n: int) -> List[str]:
        self._process_due_cashbacks(timestamp)
        accounts = self.repo.get_all_accounts()
        sorted_accs = sorted(accounts, key=lambda a: (-a.total_outgoing, a.account_id))
        return [f"{a.account_id}({a.total_outgoing})" for a in sorted_accs[:n]]
