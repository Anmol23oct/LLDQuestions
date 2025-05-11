// UserRepository.cs
using System.Collections.Generic;

public class UserRepository
{
    private readonly Dictionary<string, User> _users = new();

    public bool AddUser(string userId, int capacity)
    {
        if (_users.ContainsKey(userId)) return false;
        _users[userId] = new User(userId, capacity);
        return true;
    }

    public User? GetUser(string userId)
    {
        return _users.TryGetValue(userId, out var user) ? user : null;
    }

    public void DeleteUser(string userId)
    {
        _users.Remove(userId);
    }

    public int? MergeUsers(string user1Id, string user2Id)
    {
        if (user1Id == "admin" || user2Id == "admin") return null;
        if (!_users.ContainsKey(user1Id) || !_users.ContainsKey(user2Id)) return null;

        var user1 = _users[user1Id];
        var user2 = _users[user2Id];

        user1.MergeFrom(user2);
        DeleteUser(user2Id);

        return user1.RemainingCapacity();
    }
}
