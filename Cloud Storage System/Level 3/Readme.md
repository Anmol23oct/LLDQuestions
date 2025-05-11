
# 📘 Level 3 – Summary

## 🎯 Goal:
Add multi-user support where each user has:
- A fixed storage capacity (in bytes)
- A personal file space
- The ability to merge accounts

---

## 🧱 Architectural Overview

### ✅ User
Encapsulates user state:
- `capacity` (total limit)
- `used` (space used)
- `files` (set of file paths owned)

Exposes:
- `has_capacity(size)` → whether user can add a new file
- `add_file(path, size)` / `delete_file(path, size)`
- `remaining_capacity()`
- `merge_from(other_user)`

---

### ✅ UserRepository
Central registry of all users

Handles:
- `add_user(user_id, capacity)`
- `get_user(user_id)`
- `merge_users(user1, user2)`:
  - Transfers files
  - Adds capacity and used bytes
  - Deletes `user2`
  - Skips if `user1` or `user2` is `"admin"`

---

## 🔁 Changes to Existing System

### ✅ FileRepository (Updated)
Stores each file as `(File, owner_user_id)`

Now supports:
- Tracking ownership
- Getting all files with owners
- Deleting a file and returning its owner

---

### ✅ FileService (Updated)
Becomes the facade layer combining:
- File operations
- User validations

Adds support for:
- `add_user(user_id, capacity)`
- `add_file(user_id, path, size)`:
  - Enforces file uniqueness, capacity check, ownership
- `merge_user(user1, user2)`:
  - Calls into `UserRepository`
  - Returns new remaining capacity or `""`
- `get_largest(prefix, n)`
- `get_file_size(path)`
- `delete_file(path)`

---

## 🧪 Business Logic Recap

| Operation        | Behavior                                                       |
|------------------|----------------------------------------------------------------|
| `ADD_USER`       | Adds user if they don’t exist                                  |
| `ADD_FILE`       | Adds or overwrites file only if user has enough space          |
| `MERGE_USER`     | Transfers files, sums capacities & usage, deletes user2        |
| Ownership check  | Only file owner can overwrite                                  |
| Capacity logic   | Used on `ADD_FILE`, not required on `MERGE_USER`               |

---

## ✅ SOLID Principles

| Principle | Implementation                                                                 |
|-----------|---------------------------------------------------------------------------------|
| **SRP**   | Each class has a single responsibility (User, File, Repository, Service)       |
| **OCP**   | System is open to extension (new commands like quotas, file rename)            |
| **LSP**   | All components can be extended without breaking usage                          |
| **ISP**   | Not yet needed, but easily added (e.g., `IStorage`, `IUserAccount`)            |
| **DIP**   | Service depends on abstractions (`FileRepo`, `UserRepo`), not concrete logic   |
