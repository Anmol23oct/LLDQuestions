public class DepositTransaction : Transaction
{
    private readonly string _accountId;
    private readonly int _amount;

    public DepositTransaction(int timestamp, string accountId, int amount)
        : base(timestamp)
    {
        _accountId = accountId;
        _amount = amount;
    }

    public override int? Execute(Dictionary<string, Account> accounts)
    {
        if (!accounts.TryGetValue(_accountId, out var account))
            return null;

        account.Deposit(_amount);
        return account.GetBalance();
    }
}
