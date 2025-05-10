// FileService.cs

public class FileService
{
    private readonly FileRepository _repository;

    public FileService(FileRepository repository)
    {
        _repository = repository;
    }

    public string AddFile(string path, int size)
    {
        var file = new File(path, size);
        return _repository.Add(file) ? "true" : "false";
    }

    public string GetFileSize(string path)
    {
        var file = _repository.Get(path);
        return file != null ? file.Size.ToString() : string.Empty;
    }

    public string DeleteFile(string path)
    {
        var file = _repository.Delete(path);
        return file != null ? file.Size.ToString() : string.Empty;
    }

    public string GetLargest(string prefix, int n)
    {
        var allFiles = _repository.GetAll()
            .Where(f => f.Path.StartsWith(prefix))
            .OrderByDescending(f => f.Size)
            .ThenBy(f => f.Path)
            .Take(n)
            .Select(f => $"{f.Path}({f.Size})")
            .ToList();

        return allFiles.Count == 0 ? string.Empty : string.Join(", ", allFiles);
    }
}
