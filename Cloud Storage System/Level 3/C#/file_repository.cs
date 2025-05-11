
// FileRepository.cs
using System.Collections.Generic;

public class FileRepository
{
    private readonly Dictionary<string, (File file, string owner)> _storage = new();

    public bool Exists(string path)
    {
        return _storage.ContainsKey(path);
    }

    public bool Add(File file, string owner)
    {
        if (Exists(file.Path)) return false;
        _storage[file.Path] = (file, owner);
        return true;
    }

    public File? Get(string path)
    {
        return _storage.TryGetValue(path, out var entry) ? entry.file : null;
    }

    public string? GetOwner(string path)
    {
        return _storage.TryGetValue(path, out var entry) ? entry.owner : null;
    }

    public (File, string)? Delete(string path)
    {
        if (!_storage.TryGetValue(path, out var entry)) return null;
        _storage.Remove(path);
        return entry;
    }

    public List<(File, string)> GetAll()
    {
        return new List<(File, string)>(_storage.Values);
    }
}
