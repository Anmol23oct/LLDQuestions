// WorkerRepository.cs
using System.Collections.Generic;
using System.Linq;

public class WorkerRepository
{
    private readonly Dictionary<string, Worker> _workers = new();

    public string AddWorker(string workerId, string position, int compensation)
    {
        if (_workers.ContainsKey(workerId))
            return "false";

        _workers[workerId] = new Worker(workerId, position, compensation);
        return "true";
    }

    public Worker? GetWorker(string workerId)
    {
        return _workers.TryGetValue(workerId, out var worker) ? worker : null;
    }

    public List<Worker> GetWorkersByPosition(string position)
    {
        return _workers.Values
            .Where(w => w.GetCurrentPosition() == position)
            .ToList();
    }
}
