// Worker.cs
using System.Collections.Generic;

public class WorkSession
{
    public int Start { get; }
    public int End { get; }
    public string Position { get; }
    public int Compensation { get; }

    public WorkSession(int start, int end, string position, int compensation)
    {
        Start = start;
        End = end;
        Position = position;
        Compensation = compensation;
    }
}

public class Worker
{
    public string WorkerId { get; }
    public string Position { get; private set; }
    public int Compensation { get; private set; }
    public int TotalMinutes => _totalMinutes;

    private bool _isInside = false;
    private int? _lastEntryTime = null;
    private int _totalMinutes = 0;

    private string? _pendingPosition = null;
    private int? _pendingCompensation = null;
    private int? _promotionStartTimestamp = null;

    pri
