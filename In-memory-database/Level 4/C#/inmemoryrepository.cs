// InMemoryRepository.cs (append to class)

public Dictionary<string, Record> GetAllRecords()
{
    return _records;
}

public void SetAllRecords(Dictionary<string, Record> newRecords)
{
    _records = newRecords;
}
