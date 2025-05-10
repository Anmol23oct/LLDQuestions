// FileRepository.cs
using System.Collections.Generic;

public class FileRepository
{
    private readonly Dictionary<string, File> _storage = new();

    public bool Exists(string path)
    {
        return _storage.ContainsKey(path);
    }

    public bool Add(File file)
    {
        if (Exists(file.Path)) return false;
        _storage[file.Path] = file;
        return true;
    }

    public File? Get(string path)
    {
        return _storage.TryGetValue(path, out var file) ? file : null;
    }

    public File? Delete(string path)
    {
        if (!_storage.TryGetValue(path, out var file)) return null;
        _storage.Remove(path);
        return file;
    }
}
