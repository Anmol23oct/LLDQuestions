using System.Collections.Generic;
using System.Linq;

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

    public string Scan()
    {
        return FormatFields(_fields);
    }

    public string ScanByPrefix(string prefix)
    {
        var filtered = _fields
            .Where(kv => kv.Key.StartsWith(prefix))
            .ToDictionary(kv => kv.Key, kv => kv.Value);
        return FormatFields(filtered);
    }

    private string FormatFields(Dictionary<string, string> fields)
    {
        return string.Join(", ", fields
            .OrderBy(kv => kv.Key)
            .Select(kv => $"{kv.Key}({kv.Value})"));
    }
}
