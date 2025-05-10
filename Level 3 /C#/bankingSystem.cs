// Level 3 - Banking System with Scheduled Payments and Cashback
using System;
using System.Collections.Generic;
using System.Linq;

public class BankingSystem
{
    private readonly Dictionary<string, Account> _accounts = new();
    private readonly Dictionary<string, int> _outgoingTotals = new();
    private readonly Dictionary<string, Dictionary<string, string>> _paymentStatus = new();
    private readonly PriorityQueue<(long timestamp, string accountId, int cashback, string paymentId), long> _cashbackQueue = new();
    private long _paymentCounter = 0;
    private const long MILLISECONDS_IN_A_DAY = 86400000;

    public bool CreateAccount(int timestamp, string accountId)
    {
        if (_accounts.ContainsKey(accountId)) return false;

        _accounts[accountId] = new Account(accountId);
        _outgoingTotals[accountId] = 0;
        _paymentStatus[accountId] = new Dictionary<string, string>();
        return true;
    }

    public int? Deposit(int timestamp, string accountId, int amount)
    {
        ProcessCashbacks(timestamp);

        if (!_accounts.TryGetValue(accountId, out var account)) return null;

        account.Deposit(amount);
        return account.GetBalance();
    }

    public int? Transfer(int timestamp, string sourceId, string targetId, int amount)
    {
        ProcessCashbacks(timestamp);

        if (!_accounts.TryGetValue(sourceId, out var source) ||
            !_accounts.TryGetValue(targetId, out var target) ||
            sourceId == targetId ||
            !source.Withdraw(amount))
            return null;

        target.Deposit(amount);
        _outgoingTotals[sourceId] += amount;
        return source.GetBalance();
    }

    public List<string> TopSpenders(int timestamp, int n)
    {
        ProcessCashbacks(timestamp);

        return _outgoingTotals
            .OrderByDescending(kv => kv.Value)
            .ThenBy(kv => kv.Key)
            .Take(n)
            .Select(kv => $"{kv.Key}({kv.Value})")
            .ToList();
    }

    public string? Pay(int timestamp, string accountId, int amount)
    {
        ProcessCashbacks(timestamp);

        if (!_accounts.TryGetValue(accountId, out var account)) return null;

        if (!account.Withdraw(amount)) return null;

        _outgoingTotals[accountId] += amount;
        _paymentCounter++;

        var paymentId = $"payment{_paymentCounter}";
        var cashbackAmount = (amount * 2) / 100;
        var cashbackTimestamp = timestamp + MILLISECONDS_IN_A_DAY;

        _cashbackQueue.Enqueue((cashbackTimestamp, accountId, cashbackAmount, paymentId), cashbackTimestamp);
        _paymentStatus[accountId][paymentId] = "IN_PROGRESS";

        return paymentId;
    }

    public string? GetPaymentStatus(int timestamp, string accountId, string paymentId)
    {
        ProcessCashbacks(timestamp);

        if (!_accounts.ContainsKey(accountId) ||
            !_paymentStatus.ContainsKey(accountId) ||
            !_paymentStatus[accountId].ContainsKey(paymentId))
            return null;

        return _paymentStatus[accountId][paymentId];
    }

    private void ProcessCashbacks(long timestamp)
    {
        while (_cashbackQueue.Count > 0 && _cashbackQueue.Peek().timestamp <= timestamp)
        {
            var (cashbackTime, accountId, cashback, paymentId) = _cashbackQueue.Dequeue();
            if (_accounts.TryGetValue(accountId, out var account))
            {
                account.Deposit(cashback);
                _paymentStatus[accountId][paymentId] = "CASHBACK_RECEIVED";
            }
        }
    }
}

// Account class remains unchanged and should support Withdraw, Deposit, and GetBalance methods as implemented earlier.
