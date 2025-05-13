// Record.cs
using System.Collections.Generic;

public class Record
{
    private readonly Dictionary<string, string> _fields = new();

    public void SetField(string field, string value)
    {
        _fields[field] = value;
    }

    public string GetField(string field)
    {
        return _fields.TryGetValue(field, out var value) ? value : "";
    }

    public bool DeleteField(string field)
    {
        return _fields.Remove(field);
    }
}
