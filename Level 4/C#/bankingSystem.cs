// Level 4 - Banking System with Account Merging and Historical Balance Tracking in C#
using System;
using System.Collections.Generic;
using System.Linq;

public class BankingSystem
{
    private readonly Dictionary<string, Account> _accounts = new();
    private readonly Dictionary<string, int> _outgoingTotals = new();
    private readonly Dictionary<string, Dictionary<string, string>> _paymentStatus = new();
    private readonly PriorityQueue<(long timestamp, string accountId, int cashback, string paymentId), long> _cashbackQueue = new();
    private readonly Dictionary<string, List<(long timestamp, int balance)>> _accountHistory = new();
    private readonly Dictionary<string, string> _mergeMap = new();
    private long _paymentCounter = 0;
    private const long MILLISECONDS_IN_A_DAY = 86400000;

    private string ResolveAccount(string accountId)
    {
        while (_mergeMap.ContainsKey(accountId))
        {
            accountId = _mergeMap[accountId];
        }
        return accountId;
    }

    public bool CreateAccount(int timestamp, string accountId)
    {
        if (_accounts.ContainsKey(accountId)) return false;

        _accounts[accountId] = new Account(accountId);
        _outgoingTotals[accountId] = 0;
        _paymentStatus[accountId] = new Dictionary<string, string>();
        _accountHistory[accountId] = new List<(long, int)> { (timestamp, 0) };
        return true;
    }

    private void UpdateBalanceHistory(string accountId, long timestamp)
    {
        string resolved = ResolveAccount(accountId);
        int balance = _accounts[resolved].GetBalance();
        _accountHistory[resolved].Add((timestamp, balance));
    }

    public int? Deposit(long timestamp, string accountId, int amount)
    {
        ProcessCashbacks(timestamp);
        string resolved = ResolveAccount(accountId);
        if (!_accounts.TryGetValue(resolved, out var account)) return null;

        account.Deposit(amount);
        UpdateBalanceHistory(resolved, timestamp);
        return account.GetBalance();
    }

    public int? Transfer(long timestamp, string sourceId, string targetId, int amount)
    {
        ProcessCashbacks(timestamp);
        string src = ResolveAccount(sourceId);
        string tgt = ResolveAccount(targetId);

        if (src == tgt || !_accounts.ContainsKey(src) || !_accounts.ContainsKey(tgt)) return null;

        var source = _accounts[src];
        var target = _accounts[tgt];

        if (!source.Withdraw(amount)) return null;

        target.Deposit(amount);
        _outgoingTotals[src] += amount;
        UpdateBalanceHistory(src, timestamp);
        UpdateBalanceHistory(tgt, timestamp);
        return source.GetBalance();
    }

    public string? Pay(long timestamp, string accountId, int amount)
    {
        ProcessCashbacks(timestamp);
        string resolved = ResolveAccount(accountId);
        if (!_accounts.TryGetValue(resolved, out var account)) return null;
        if (!account.Withdraw(amount)) return null;

        _outgoingTotals[resolved] += amount;
        _paymentCounter++;
        string paymentId = $"payment{_paymentCounter}";
        long cashbackTime = timestamp + MILLISECONDS_IN_A_DAY;
        int cashbackAmount = (amount * 2) / 100;

        _cashbackQueue.Enqueue((cashbackTime, resolved, cashbackAmount, paymentId), cashbackTime);
        _paymentStatus[resolved][paymentId] = "IN_PROGRESS";
        UpdateBalanceHistory(resolved, timestamp);
        return paymentId;
    }

    public string? GetPaymentStatus(long timestamp, string accountId, string paymentId)
    {
        ProcessCashbacks(timestamp);
        string resolved = ResolveAccount(accountId);
        return _paymentStatus.ContainsKey(resolved) && _paymentStatus[resolved].ContainsKey(paymentId)
            ? _paymentStatus[resolved][paymentId]
            : null;
    }

    public List<string> TopSpenders(long timestamp, int n)
    {
        ProcessCashbacks(timestamp);
        var mergedTotals = new Dictionary<string, int>();
        foreach (var kvp in _outgoingTotals)
        {
            string root = ResolveAccount(kvp.Key);
            if (!mergedTotals.ContainsKey(root)) mergedTotals[root] = 0;
            mergedTotals[root] += kvp.Value;
        }
        return mergedTotals
            .OrderByDescending(kv => kv.Value)
            .ThenBy(kv => kv.Key)
            .Take(n)
            .Select(kv => $"{kv.Key}({kv.Value})")
            .ToList();
    }

    public int? GetBalance(long timestamp, string accountId, long timeAt)
    {
        string resolved = ResolveAccount(accountId);
        if (!_accountHistory.ContainsKey(resolved)) return null;

        int? result = null;
        foreach (var (ts, bal) in _accountHistory[resolved])
        {
            if (ts <= timeAt) result = bal;
            else break;
        }
        return result;
    }

    public bool MergeAccounts(long timestamp, string acc1, string acc2)
    {
        string root1 = ResolveAccount(acc1);
        string root2 = ResolveAccount(acc2);
        if (root1 == root2 || !_accounts.ContainsKey(root1) || !_accounts.ContainsKey(root2)) return false;

        _accounts[root1].Deposit(_accounts[root2].GetBalance());
        _outgoingTotals[root1] += _outgoingTotals.GetValueOrDefault(root2);

        foreach (var kv in _paymentStatus[root2])
        {
            _paymentStatus[root1][kv.Key] = kv.Value;
        }
        foreach (var entry in _accountHistory[root2])
        {
            _accountHistory[root1].Add((timestamp, _accounts[root1].GetBalance()));
        }
        _mergeMap[root2] = root1;

        _accounts.Remove(root2);
        _outgoingTotals.Remove(root2);
        _paymentStatus.Remove(root2);
        _accountHistory.Remove(root2);
        return true;
    }

    private void ProcessCashbacks(long timestamp)
    {
        while (_cashbackQueue.Count > 0 && _cashbackQueue.Peek().timestamp <= timestamp)
        {
            var (cashbackTime, accountId, cashback, paymentId) = _cashbackQueue.Dequeue();
            string resolved = ResolveAccount(accountId);
            if (_accounts.ContainsKey(resolved))
            {
                _accounts[resolved].Deposit(cashback);
                _paymentStatus[resolved][paymentId] = "CASHBACK_RECEIVED";
                UpdateBalanceHistory(resolved, cashbackTime);
            }
        }
    }
}

// Account class remains unchanged and should support Withdraw, Deposit, and GetBalance methods as implemented earlier.

