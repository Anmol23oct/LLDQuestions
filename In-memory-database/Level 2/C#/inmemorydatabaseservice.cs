public class InMemoryDatabaseService
{
    private readonly InMemoryRepository _repository;

    public InMemoryDatabaseService(InMemoryRepository repository)
    {
        _repository = repository;
    }

    public string Set(string key, string field, string value)
    {
        var record = _repository.GetOrCreate(key);
        record.SetField(field, value);
        return "";
    }

    public string Get(string key, string field)
    {
        var record = _repository.GetRecord(key);
        return record?.GetField(field) ?? "";
    }

    public string Delete(string key, string field)
    {
        var record = _repository.GetRecord(key);
        return record != null && record.DeleteField(field) ? "true" : "false";
    }

    public string Scan(string key)
    {
        var record = _repository.GetRecord(key);
        return record?.Scan() ?? "";
    }

    public string ScanByPrefix(string key, string prefix)
    {
        var record = _repository.GetRecord(key);
        return record?.ScanByPrefix(prefix) ?? "";
    }
}
