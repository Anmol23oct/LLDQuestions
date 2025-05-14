// InMemoryDatabaseService.cs

public class InMemoryDatabaseService
{
    private readonly InMemoryRepository _repository;

    public InMemoryDatabaseService(InMemoryRepository repository)
    {
        _repository = repository;
    }

    public string Set(string key, string field, string value)
    {
        return SetAt(key, field, value, null);
    }

    public string SetAt(string key, string field, string value, int? timestamp)
    {
        var record = _repository.GetOrCreate(key);
        record.SetField(field, value, timestamp);
        return "";
    }

    public string SetAtWithTTL(string key, string field, string value, int timestamp, int ttl)
    {
        var record = _repository.GetOrCreate(key);
        record.SetField(field, value, timestamp, ttl);
        return "";
    }

    public string Get(string key, string field)
    {
        return GetAt(key, field, null);
    }

    public string GetAt(string key, string field, int? timestamp)
    {
        var record = _repository.GetRecord(key);
        return record?.GetField(field, timestamp) ?? "";
    }

    public string Delete(string key, string field)
    {
        return DeleteAt(key, field, null);
    }

    public string DeleteAt(string key, string field, int? timestamp)
    {
        var record = _repository.GetRecord(key);
        return record != null && record.DeleteField(field, timestamp) ? "true" : "false";
    }

    public string Scan(string key)
    {
        return ScanAt(key, null);
    }

    public string ScanAt(string key, int? timestamp)
    {
        var record = _repository.GetRecord(key);
        return record?.Scan(timestamp) ?? "";
    }

    public string ScanByPrefix(string key, string prefix)
    {
        return ScanByPrefixAt(key, prefix, null);
    }

    public string ScanByPrefixAt(string key, string prefix, int? timestamp)
    {
        var record = _repository.GetRecord(key);
        return record?.ScanByPrefix(prefix, timestamp) ?? "";
    }
}
