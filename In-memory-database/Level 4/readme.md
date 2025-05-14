# 🗃️ In-Memory Database – Level 4: Backup & Restore

## ✅ Objective

Enable the in-memory database to **backup** the current state and **restore** it later. When restoring, TTLs should be recalculated to reflect remaining lifetime.

---

## 📦 New Operations

| Operation                                         | Description                                                                                                                   |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `BACKUP <timestamp>`                              | Takes a snapshot of all current records and their remaining TTLs. Returns the number of non-empty records saved.              |
| `RESTORE <currentTimestamp> <timestampToRestore>` | Restores the most recent backup taken on or before `timestampToRestore`. Recalculates expiration based on `currentTimestamp`. |

---

## 🧱 Architecture Changes

### ✅ `Record` (updated)

* Added `clone_with_remaining_ttl(at_time)` to create a new `Record` with TTLs adjusted relative to the backup time.

### ✅ `InMemoryRepository` (updated)

* Added `get_all_records()` and `set_all_records()` to allow bulk retrieval and replacement of the in-memory database.

### ✅ `BackupManager` (new)

* Stores snapshots of the entire in-memory database.
* Each snapshot keeps the TTL-relative state of each field.
* Supports `save_snapshot(timestamp)` and `get_snapshot_before_or_at(restoreTime)`.

### ✅ `InMemoryDatabaseService` (updated)

* Added:
  * `backup(timestamp)` → triggers `BackupManager.save_snapshot()`
  * `restore(now, timestampToRestore)` → gets the appropriate snapshot and rebuilds the repository with TTLs adjusted relative to `now`.

---

## 🧪 Example Behavior

| Query                        | Explanation                                           |
| ---------------------------- | ----------------------------------------------------- |
| `SET_AT_WITH_TTL A B C 1 10` | Field B expires at 11                                 |
| `BACKUP 3`                   | Saves snapshot with 8ms TTL remaining                 |
| `DELETE_AT A B 8`            | Deletes field B manually                              |
| `RESTORE 10 3`               | Restores field B and sets new expiry to `10 + 8 = 18` |

---

## ✅ Design Principles Followed

| Principle        | Application                                                         |
| ---------------- | ------------------------------------------------------------------- |
| SRP              | `BackupManager` handles backup state only, not DB logic             |
| OCP              | Easy to add future enhancements like named snapshots or persistence |
| DIP              | `InMemoryDatabaseService` delegates TTL tracking to other layers    |
| Clean Separation | Database logic and backup logic are modular and testable            |

---

✅ Fully supports time-aware recovery and maintains TTL consistency across snapshots.

➡️ Ready to move to persistence or audit logging features if needed.
