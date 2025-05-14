// Record.cs (append inside Record class)

public Record CloneWithRemainingTTL(int atTime)
{
    var newRecord = new Record();

    foreach (var (field, fieldObj) in _fields)
    {
        if (!fieldObj.IsValid(atTime)) continue;

        int? ttlRemaining = fieldObj.ExpiresAt.HasValue
            ? fieldObj.ExpiresAt.Value - atTime
            : null;

        newRecord.SetField(field, fieldObj.Value, 0, ttlRemaining);
    }

    return newRecord._fields.Count > 0 ? newRecord : null;
}
