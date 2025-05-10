using System.Collections.Generic;

public abstract class Transaction
{
    public int Timestamp { get; }

    protected Transaction(int timestamp)
    {
        Timestamp = timestamp;
    }

    public abstract int? Execute(Dictionary<string, Account> accounts);
}
