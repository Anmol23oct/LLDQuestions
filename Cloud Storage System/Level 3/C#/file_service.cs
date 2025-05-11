// FileService.cs
using System.Linq;

public class FileService
{
    private readonly FileRepository _fileRepo;
    private readonly UserRepository _userRepo;

    public FileService(FileRepository fileRepo, UserRepository userRepo)
    {
        _fileRepo = fileRepo;
        _userRepo = userRepo;
    }

    public string AddUser(string userId, int capacity)
    {
        return _userRepo.AddUser(userId, capacity) ? "true" : "false";
    }

    public string AddFile(string userId, string path, int size)
    {
        var user = _userRepo.GetUser(userId);
        if (user == null) return "";

        if (_fileRepo.Exists(path))
        {
            var oldFile = _fileRepo.Get(path);
            var owner = _fileRepo.GetOwner(path);
            if (owner != userId) return "";
            user.DeleteFile(path, oldFile!.Size);
        }

        if (!user.HasCapacity(size)) return "";

        var newFile = new File(path, size);
        _fileRepo.Add(newFile, userId);
        user.AddFile(path, size);

        return user.RemainingCapacity().ToString();
    }

    public string DeleteFile(string path)
    {
        var entry = _fileRepo.Delete(path);
        if (entry == null) return "";

        var (file, ownerId) = entry.Value;
        var owner = _userRepo.GetUser(ownerId);
        owner?.DeleteFile(path, file.Size);
        return file.Size.ToString();
    }

    public string GetFileSize(string path)
    {
        var file = _fileRepo.Get(path);
        return file != null ? file.Size.ToString() : string.Empty;
    }

    public string GetLargest(string prefix, int n)
    {
        var allFiles = _fileRepo.GetAll()
            .Where(x => x.Item1.Path.StartsWith(prefix))
            .OrderByDescending(x => x.Item1.Size)
            .ThenBy(x => x.Item1.Path)
            .Take(n)
            .Select(x => $"{x.Item1.Path}({x.Item1.Size})")
            .ToList();

        return allFiles.Count == 0 ? string.Empty : string.Join(", ", allFiles);
    }

    public string MergeUser(string user1Id, string user2Id)
    {
        var result = _userRepo.MergeUsers(user1Id, user2Id);
        return result.HasValue ? result.Value.ToString() : string.Empty;
    }
}
