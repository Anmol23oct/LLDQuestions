// Worker.cs
public class Worker
{
    public string WorkerId { get; }
    public string Position { get; }
    public int Compensation { get; }
    public int TotalMinutes => _totalMinutes;

    private bool _isInside = false;
    private int? _lastEntryTime = null;
    private int _totalMinutes = 0;

    public Worker(string workerId, string position, int compensation)
    {
        WorkerId = workerId;
        Position = position;
        Compensation = compensation;
    }

    public string Register(int timestamp)
    {
        if (!_isInside)
        {
            _isInside = true;
            _lastEntryTime = timestamp;
        }
        else
        {
            if (_lastEntryTime.HasValue)
            {
                _totalMinutes += timestamp - _lastEntryTime.Value;
                _lastEntryTime = null;
            }
            _isInside = false;
        }

        return "registered";
    }

    public string GetTotalMinutes()
    {
        return _totalMinutes.ToString();
    }
}
