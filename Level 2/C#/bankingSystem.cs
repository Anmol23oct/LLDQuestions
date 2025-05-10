// Assuming we already have Account.cs, Transaction.cs, DepositTransaction.cs, TransferTransaction.cs as defined before

using System;
using System.Collections.Generic;
using System.Linq;

public class BankingSystem
{
    private readonly Dictionary<string, Account> _accounts = new();
    private readonly Dictionary<string, int> _outgoingTotals = new();

    public bool CreateAccount(int timestamp, string accountId)
    {
        if (_accounts.ContainsKey(accountId))
            return false;

        _accounts[accountId] = new Account(accountId);
        _outgoingTotals[accountId] = 0;
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
        var result = transaction.Execute(_accounts);

        if (result.HasValue)
        {
            if (_outgoingTotals.ContainsKey(sourceId))
                _outgoingTotals[sourceId] += amount;
        }

        return result;
    }

    public List<string> TopSpenders(int timestamp, int n)
    {
        return _outgoingTotals
            .OrderByDescending(kv => kv.Value)
            .ThenBy(kv => kv.Key)
            .Take(n)
            .Select(kv => $"{kv.Key}({kv.Value})")
            .ToList();
    }
}

// Sample usage (outside class)
/*
var bank = new BankingSystem();
bank.CreateAccount(1, "account3");
bank.CreateAccount(2, "account2");
bank.CreateAccount(3, "account1");
bank.Deposit(4, "account3", 2000);
bank.Deposit(5, "account2", 3000);
bank.Deposit(6, "account3", 4000);
Console.WriteLine(string.Join(", ", bank.TopSpenders(7, 3))); // [account1(0), account2(0), account3(0)]
bank.Transfer(8, "account3", "account2", 500);
bank.Transfer(9, "account3", "account1", 1000);
bank.Transfer(10, "account1", "account2", 2500);
Console.WriteLine(string.Join(", ", bank.TopSpenders(11, 3))); // [account1(2500), account3(1500), account2(0)]
*/
