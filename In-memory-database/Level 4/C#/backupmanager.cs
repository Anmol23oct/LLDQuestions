// BackupManager.cs
using System.Collections.Generic;
using System.Linq;

public class BackupManager
{
    private readonly List<(int Timestamp, Dictionary<string, Record> Snapshot)> _backups = new();

    public int SaveSnapshot(int timestamp, Dictionary<string, Record> currentData)
    {
        var snapshot = new Dictionary<string, Record>();

        foreach (var (key, record) in currentData)
        {
            var filtered = record.CloneWithRemainingTTL(timestamp);
            if (filtered != null)
            {
                snapshot[key] = filtered;
            }
        }

        _backups.Add((timestamp, snapshot));
        return snapshot.Count;
    }

    public (int, Dictionary<string, Record>)? GetSnapshotBeforeOrAt(int timestamp)
    {
        (int, Dictionary<string, Record>)? result = null;

        foreach (var (ts, snap) in _backups)
        {
            if (ts <= timestamp)
                result = (ts, snap);
            else
                break;
        }

        return result;
    }
}
