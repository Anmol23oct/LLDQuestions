# 📁 User Backup & Restore System

## 🎯 Goal

Allow users to **back up and restore their files independently** of other users.

---

## 📘 Features

| Operation               | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `BACKUP_USER <userId>`  | Saves the user’s currently owned files (`path → size`). Overwrites any previous backup. |
| `RESTORE_USER <userId>` | Replaces the user's current files with their most recent backup (if it exists). Skips restoring files owned by someone else. |
| ✅ Handles deleted users' file cleanup | Files owned by deleted or merged users are removed from the system. |

---

## 💡 Why This Matters

- 🧹 **Prevents storage bloat** by removing ghost files.
- 🛠️ **Maintains clean ownership mapping** across the system.
- 🔄 **Ensures future operations** like `ADD_FILE` and `RESTORE_USER` behave consistently.

