// InMemoryRepository.cs
using System.Collections.Generic;

public class InMemoryRepository
{
    private readonly Dictionary<string, Record> _records = new();

    public Record GetOrCreate(string key)
    {
        if (!_records.ContainsKey(key))
        {
            _records[key] = new Record();
        }
        return _records[key];
    }

    public Record? GetRecord(string key)
    {
        return _records.TryGetValue(key, out var record) ? record : null;
    }
}
