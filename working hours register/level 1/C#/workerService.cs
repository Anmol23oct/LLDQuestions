// WorkerService.cs
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
}
