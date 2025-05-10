public class Account
{
    public string AccountId { get; }
    private int _balance;

    public Account(string accountId)
    {
        AccountId = accountId;
        _balance = 0;
    }

    public void Deposit(int amount)
    {
        _balance += amount;
    }

    public bool CanWithdraw(int amount)
    {
        return _balance >= amount;
    }

    public bool Withdraw(int amount)
    {
        if (CanWithdraw(amount))
        {
            _balance -= amount;
            return true;
        }
        return false;
    }

    public int GetBalance()
    {
        return _balance;
    }
}
