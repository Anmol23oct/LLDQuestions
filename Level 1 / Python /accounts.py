# account.py

class Account:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0

    def deposit(self, amount: int):
        self.balance += amount

    def can_withdraw(self, amount: int) -> bool:
        return self.balance >= amount

    def withdraw(self, amount: int) -> bool:
        if self.can_withdraw(amount):
            self.balance -= amount
            return True
        return False

    def get_balance(self) -> int:
        return self.balance
