# banking_system.py

from account import Account
from transactions import DepositTransaction, TransferTransaction
import heapq

class BankingSystem:
    def __init__(self):
        self.accounts = {}  # account_id -> Account
        self.outgoing_totals = {}  # account_id -> int
        self.payment_counter = 0
        self.scheduled_cashbacks = []  # min-heap of (timestamp, account_id, amount, payment_id)
        self.payment_status = {}  # account_id -> {payment_id: status}
        self.account_history = {}  # account_id -> list of (timestamp, balance)
        self.merge_map = {}  # merged_id -> active_id

    def _resolve_account(self, account_id):
        while account_id in self.merge_map:
            account_id = self.merge_map[account_id]
        return account_id

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account(account_id)
        self.outgoing_totals[account_id] = 0
        self.payment_status[account_id] = {}
        self.account_history[account_id] = [(timestamp, 0)]
        return True

    def _update_balance_history(self, account_id, timestamp):
        resolved = self._resolve_account(account_id)
        balance = self.accounts[resolved].get_balance()
        self.account_history[resolved].append((timestamp, balance))

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._process_cashbacks(timestamp)
        resolved = self._resolve_account(account_id)
        if resolved not in self.accounts:
            return None
        self.accounts[resolved].deposit(amount)
        self._update_balance_history(resolved, timestamp)
        return self.accounts[resolved].get_balance()

    def transfer(self, timestamp: int, source_id: str, target_id: str, amount: int) -> int | None:
        self._process_cashbacks(timestamp)
        s_id, t_id = self._resolve_account(source_id), self._resolve_account(target_id)
        if s_id == t_id or s_id not in self.accounts or t_id not in self.accounts:
            return None
        if not self.accounts[s_id].can_withdraw(amount):
            return None
        self.accounts[s_id].withdraw(amount)
        self.accounts[t_id].deposit(amount)
        self.outgoing_totals[s_id] += amount
        self._update_balance_history(s_id, timestamp)
        self._update_balance_history(t_id, timestamp)
        return self.accounts[s_id].get_balance()

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        self._process_cashbacks(timestamp)
        merged_totals = {}
        for acc, total in self.outgoing_totals.items():
            active = self._resolve_account(acc)
            merged_totals[active] = merged_totals.get(active, 0) + total
        sorted_accounts = sorted(merged_totals.items(), key=lambda x: (-x[1], x[0]))
        return [f"{k}({v})" for k, v in sorted_accounts[:n]]

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        self._process_cashbacks(timestamp)
        resolved = self._resolve_account(account_id)
        if resolved not in self.accounts:
            return None
        if not self.accounts[resolved].can_withdraw(amount):
            return None
        self.accounts[resolved].withdraw(amount)
        self.outgoing_totals[resolved] += amount
        self.payment_counter += 1
        payment_id = f"payment{self.payment_counter}"
        cashback_time = timestamp + 86400000
        cashback = amount * 2 // 100
        heapq.heappush(self.scheduled_cashbacks, (cashback_time, resolved, cashback, payment_id))
        self.payment_status[resolved][payment_id] = "IN_PROGRESS"
        self._update_balance_history(resolved, timestamp)
        return payment_id

    def get_payment_status(self, timestamp: int, account_id: str, payment_id: str) -> str | None:
        self._process_cashbacks(timestamp)
        resolved = self._resolve_account(account_id)
        if resolved not in self.accounts:
            return None
        return self.payment_status.get(resolved, {}).get(payment_id)

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        resolved = self._resolve_account(account_id)
        if resolved not in self.account_history:
            return None
        history = self.account_history[resolved]
        result = None
        for t, bal in history:
            if t <= time_at:
                result = bal
            else:
                break
        return result

    def merge_accounts(self, timestamp: int, acc1: str, acc2: str) -> bool:
        root1 = self._resolve_account(acc1)
        root2 = self._resolve_account(acc2)
        if root1 == root2 or root1 not in self.accounts or root2 not in self.accounts:
            return False
        self.accounts[root1].deposit(self.accounts[root2].get_balance())
        self.outgoing_totals[root1] += self.outgoing_totals.get(root2, 0)
        for pid, status in self.payment_status[root2].items():
            self.payment_status[root1][pid] = status
        for t, bal in self.account_history[root2]:
            self.account_history[root1].append((timestamp, self.accounts[root1].get_balance()))
        self.merge_map[root2] = root1
        del self.accounts[root2]
        del self.outgoing_totals[root2]
        del self.payment_status[root2]
        del self.account_history[root2]
        return True

    def _process_cashbacks(self, timestamp: int):
        while self.scheduled_cashbacks and self.scheduled_cashbacks[0][0] <= timestamp:
            _, acc_id, cashback, pid = heapq.heappop(self.scheduled_cashbacks)
            resolved = self._resolve_account(acc_id)
            if resolved in self.accounts:
                self.accounts[resolved].deposit(cashback)
                self.payment_status[resolved][pid] = "CASHBACK_RECEIVED"
                self._update_balance_history(resolved, _)
