// User.cs
using System.Collections.Generic;
using System.Linq;

public class User
{
    public string UserId { get; }
    public int Capacity { get; private set; }
    public int Used { get; private set; }
    public HashSet<string> Files { get; } = new();

    private Dictionary<string, int>? _backup = null;

    public User(string userId, int capacity)
    {
        UserId = userId;
        Capacity = capacity;
        Used = 0;
    }

    public bool HasCapacity(int size) => (Capacity - Used) >= size;

    public void AddFile(string path, int size)
    {
        Files.Add(path);
        Used += size;
    }

    public void DeleteFile(string path, int size)
    {
        if (Files.Contains(path))
        {
            Files.Remove(path);
            Used -= size;
        }
    }

    public int RemainingCapacity() => Capacity - Used;

    public void MergeFrom(User other)
    {
        foreach (var file in other.Files)
        {
            Files.Add(file);
        }
        Used += other.Used;
        Capacity += other.Capacity;
    }

    public int Backup(Dictionary<string, int> fileSizes)
    {
        _backup = Files
            .Where(path => fileSizes.ContainsKey(path))
            .ToDictionary(path => path, path => fileSizes[path]);
        return _backup.Count;
    }

    public int Restore(
        Func<string, string?> getOwner,
        Action<string, int> restoreFile)
    {
        if (_backup == null) return 0;

        foreach (var path in Files.ToList())
        {
            DeleteFile(path, 0);
        }

        int restored = 0;
        foreach (var (path, size) in _backup)
        {
            var owner = getOwner(path);
            if (owner == null || owner == UserId)
            {
                AddFile(path, size);
                restoreFile(path, size);
                restored++;
            }
        }

        return restored;
    }
}
