// WorkerService.cs
using System.Collections.Generic;
using System.Linq;

public class WorkerService
{
    private readonly WorkerRepository _repo;

    public WorkerService(WorkerRepository repo)
    {
        _repo = repo;
    }

    public string AddWorker(string workerId, string position, int compensation)
    {
        return _repo.AddWorker(workerId, position, compensation);
    }

    public string Register(string workerId, int timestamp)
    {
        var worker = _repo.GetWorker(workerId);
        return worker != null ? worker.Register(timestamp) : "invalid_request";
    }

    public string GetTime(string workerId)
    {
        var worker = _repo.GetWorker(workerId);
        return worker != null ? worker.GetTotalMinutes() : "";
    }

    public string TopNWorkers(int n, string position)
    {
        var workers = _repo.GetWorkersByPosition(position);
        if (!workers.Any()) return "";

        var minHeap = new SortedSet<(int totalMinutes, string workerId, Worker worker)>(
            new WorkerEntryComparer()
        );

        foreach (var worker in workers)
        {
            var entry = (worker.TotalMinutes, worker.WorkerId, worker);
            minHeap.Add(entry);

            if (minHeap.Count > n)
            {
                // Remove the one with the smallest totalMinutes or largest workerId
                minHeap.Remove(minHeap.Max);
            }
        }

        var result = minHeap
            .OrderByDescending(x => x.totalMinutes)
            .ThenBy(x => x.workerId)
            .Select(x => $"{x.workerId}({x.totalMinutes})");

        return string.Join(", ", result);
    }
}
