// Record.cs
using System.Collections.Generic;
using System.Linq;

public class Record
{
    private readonly Dictionary<string, RecordField> _fields = new();

    public void SetField(string field, string value, int? timestamp = null, int? ttl = null)
    {
        int? expiresAt = ttl.HasValue && timestamp.HasValue ? timestamp + ttl : null;
        _fields[field] = new RecordField(value, expiresAt);
    }

    public string GetField(string field, int? timestamp = null)
    {
        if (!_fields.ContainsKey(field)) return "";
        var entry = _fields[field];
        return (timestamp == null || entry.IsValid(timestamp.Value)) ? entry.Value : "";
    }

    public bool DeleteField(string field, int? timestamp = null)
    {
        if (!_fields.ContainsKey(field)) return false;
        if (timestamp != null && !_fields[field].IsValid(timestamp.Value)) return false;
        return _fields.Remove(field);
    }

    public string Scan(int? timestamp = null)
    {
        return FormatFields(_fields
            .Where(kv => timestamp == null || kv.Value.IsValid(timestamp.Value))
            .ToDictionary(kv => kv.Key, kv => kv.Value));
    }

    public string ScanByPrefix(string prefix, int? timestamp = null)
    {
        var filtered = _fields
            .Where(kv => kv.Key.StartsWith(prefix)
                      && (timestamp == null || kv.Value.IsValid(timestamp.Value)))
            .ToDictionary(kv => kv.Key, kv => kv.Value);
        return FormatFields(filtered);
    }

    private string FormatFields(Dictionary<string, RecordField> fields)
    {
        return string.Join(", ",
            fields.OrderBy(kv => kv.Key)
                  .Select(kv => $"{kv.Key}({kv.Value.Value})"));
    }
}
