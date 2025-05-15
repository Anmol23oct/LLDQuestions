// WorkerEntryComparer.cs
using System.Collections.Generic;

public class WorkerEntryComparer : IComparer<(int totalMinutes, string workerId, Worker worker)>
{
    public int Compare((int totalMinutes, string workerId, Worker worker) x, (int totalMinutes, string workerId, Worker worker) y)
    {
        // Compare by totalMinutes ascending for min-heap behavior
        int cmp = x.totalMinutes.CompareTo(y.totalMinutes);
        if (cmp != 0) return cmp;

        // If totalMinutes are equal, compare by descending workerId (we'll remove Max later)
        return y.workerId.CompareTo(x.workerId);
    }
}
