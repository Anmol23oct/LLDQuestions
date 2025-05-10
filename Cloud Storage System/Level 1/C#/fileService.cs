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
}
