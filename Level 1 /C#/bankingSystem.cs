using System.Collections.Generic;

public class BankingSystem
{
    private readonly Dictionary<string, Account> _accounts = new();

    public bool CreateAccount(int timestamp, string accountId)
    {
        if (_accounts.ContainsKey(accountId))
            return false;

        _accounts[accountId] = new Account(accountId);
        return true;
    }

    public int? Deposit(int timestamp, string accountId, int amount)
    {
        var transaction = new DepositTransaction(timestamp, accountId, amount);
        return transaction.Execute(_accounts);
    }

    public int? Transfer(int timestamp, string sourceId, string targetId, int amount)
    {
        var transaction = new TransferTransaction(timestamp, sourceId, targetId, amount);
        return transaction.Execute(_accounts);
    }
}
