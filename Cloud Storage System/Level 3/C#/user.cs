// User.cs
using System.Collections.Generic;

public class User
{
    public string UserId { get; }
    public int Capacity { get; private set; }
    public int Used { get; private set; }
    public HashSet<string> Files { get; } = new();

    public User(string userId, int capacity)
    {
        UserId = userId;
        Capacity = capacity;
        Used = 0;
    }

    public bool HasCapacity(int size)
    {
        return (Capacity - Used) >= size;
    }

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

    public int RemainingCapacity()
    {
        return Capacity - Used;
    }

    public void MergeFrom(User other)
    {
        foreach (var file in other.Files)
        {
            Files.Add(file);
        }
        Used += other.Used;
        Capacity += other.Capacity;
    }
}
