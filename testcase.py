if __name__ == "__main__":
    bank = BankingSystem()
    print(bank.create_account(1, "acc1"))  # True
    print(bank.create_account(2, "acc2"))  # True
    print(bank.deposit(3, "acc1", 1000))   # 1000
    print(bank.transfer(4, "acc1", "acc2", 300))  # 700
    print(bank.transfer(5, "acc1", "acc1", 300))  # None (same account)
    print(bank.transfer(6, "acc1", "acc2", 1000))  # None (insufficient)
