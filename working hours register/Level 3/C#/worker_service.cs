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

    public string Promote(string workerId, string newPosition, int compensation, int startTimestamp)
    {
        var worker = _repo.GetWorker(workerId);
        return worker != null ? worker.Promote(newPosition, compensation, startTimestamp) : "invalid_request";
    }

    public string CalcSalary(string workerId, int start, int end)
    {
        var worker = _repo.GetWorker(workerId);
        return worker != null ? worker.CalcSalary(start, end) : "";
    }

    public string TopNWorkers(int n, string position)
    {
        var workers = _repo.GetWorkersByPosition(position);
        if (workers.Count == 0)
            return "";

        var topN = workers
            .OrderByDescending(w => w.TotalMinutes)
            .ThenBy(w => w.WorkerId)
            .Take(n)
            .Select(w => $"{w.WorkerId}({w.TotalMinutes})");

        return string.Join(", ", topN);
    }
}
