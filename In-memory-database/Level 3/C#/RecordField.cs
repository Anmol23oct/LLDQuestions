// RecordField.cs
public class RecordField
{
    public string Value { get; }
    public int? ExpiresAt { get; }

    public RecordField(string value, int? expiresAt = null)
    {
        Value = value;
        ExpiresAt = expiresAt;
    }

    public bool IsValid(int timestamp)
    {
        return ExpiresAt == null || timestamp < ExpiresAt;
    }
}
