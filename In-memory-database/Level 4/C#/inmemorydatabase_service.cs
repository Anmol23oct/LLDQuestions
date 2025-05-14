// InMemoryDatabaseService.cs (add inside class)

private readonly BackupManager _backupMgr = new();

public string Backup(int timestamp)
{
    var count = _backupMgr.SaveSnapshot(timestamp, _repository.GetAllRecords());
    return count.ToString();
}

public string Restore(int now, int restoreTime)
{
    var snapshotEntry = _backupMgr.GetSnapshotBeforeOrAt(restoreTime);
    if (!snapshotEntry.HasValue) return "";

    var (snapshotTime, snapshot) = snapshotEntry.Value;
    var restored = new Dictionary<string, Record>();

    foreach (var (key, record) in snapshot)
    {
        var updated = record.CloneWithRemainingTTL(snapshotTime);
        if (updated != null)
        {
            foreach (var field in updated.GetAllFields())
            {
                if (field.ExpiresAt.HasValue)
                    field.ExpiresAt = now + (field.ExpiresAt.Value - snapshotTime);
            }
            restored[key] = updated;
        }
    }

    _repository.SetAllRecords(restored);
    return "";
}
