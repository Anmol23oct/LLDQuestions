// File.cs

public class File
{
    public string Path { get; }
    public int Size { get; }

    public File(string path, int size)
    {
        Path = path;
        Size = size;
    }
}
