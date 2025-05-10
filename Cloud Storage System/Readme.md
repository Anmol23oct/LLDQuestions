
# 🗄️ Cloud Storage System – Multi-Level Specification

This project implements a cloud storage system that supports a range of features from basic file manipulation to multi-user management, file statistics, account merging, and backup/restore functionalities.

---

## 📘 Level 1 – Basic File Operations

The cloud storage system should support file manipulation:

- `ADD_FILE <name> <size>`  
  Adds a new file `name` to the storage with memory size `size` in bytes.  
  Returns `"true"` if added successfully, or `"false"` if the file already exists.

- `GET_FILE_SIZE <name>`  
  Returns the file size as a string if it exists, or an empty string otherwise.

- `DELETE_FILE <name>`  
  Deletes the file and returns the deleted file size. Returns an empty string if the file does not exist.

### 🔍 Example

```python
queries = [
  ["ADD_FILE", "/dir1/dir2/file.txt", "10"],
  ["ADD_FILE", "/dir1/dir2/file.txt", "5"],
  ["GET_FILE_SIZE", "/dir1/dir2/file.txt"],
  ["GET_FILE_SIZE", "/non-existing.file"],
  ["DELETE_FILE", "/dir1/dir2/file.txt"],
  ["GET_FILE_SIZE", "/dir1/dir2/file.txt"],
]
```

Output:

```json
["true", "false", "10", "", "10", ""]
```

## 📗 Level 2 – File Statistics by Prefix

Implement an operation for retrieving file statistics:

**GET_LARGEST <prefix> <n>**  
Returns the top n largest files (by size) with names starting with the prefix, formatted as:  
`"<name1>(<size1>), ..., <nameN>(<sizeN>)"`  
Sorted by size descending; ties sorted lexicographically.  
Returns empty string if no such files exist.

### 🔍 Example

```python
queries = [
  ["ADD_FILE", "/dir/file.txt", "5"],
  ["ADD_FILE", "/dir/file2.txt", "7"],
  ["ADD_FILE", "/dir/Deeper/file.x", "20"],
  ["ADD_FILE", "/big_file.mp4", "20"],
  ["GET_LARGEST", "/dir/", "2"],
  ["GET_LARGEST", "/another_dir", "5"],
  ["GET_LARGEST", "/", "3"],
  ["ADD_FILE", "/dir/file.txt", "5"],
  ["ADD_FILE", "/dir/file3.txt", "20"],
  ["GET_LARGEST", "/dir/", "7"],
]
```

Output:

```json
[
  "true", "true", "true", "true",
  "/dir/Deeper/file.x(20), /dir/file2.txt(7)",
  "",
  "/big_file.mp4(20), /dir/Deeper/file.x(20), /dir/file2.txt(7)",
  "true", "true",
  "/dir/file3.txt(20), /dir/Deeper/file.x(20), /dir/file2.txt(7)"
]
```

## 📙 Level 3 – Multi-User Support and Account Merging

Support for queries from different users. Each user is assigned a storage capacity limit.

**ADD_USER <userId> <capacity>**  
Adds a new user with given capacity in bytes. Returns "true" if successful, "false" if user exists.

**ADD_FILE <userId> <name> <size>**  
Adds a file for the specified user if they have enough capacity.  
Returns remaining capacity if successful, otherwise an empty string.

**MERGE_USER <userId1> <userId2>**  
Merges userId2 into userId1. Transfers all files and remaining capacity. Deletes userId2.  
Returns updated remaining capacity of userId1, or an empty string on failure.  
(Note: Neither user can be "admin")

### 🔍 Example

```python
queries = [
  ["ADD_USER", "user1", "200"],
  ["ADD_USER", "user1", "300"],
  ["ADD_FILE", "user1", "/file.txt", "150"],
  ["ADD_FILE", "user1", "/file2.txt", "60"],
  ["ADD_FILE", "user1", "/file3.txt", "30"],
  ["ADD_FILE", "user1", "/file2.txt", "10"],
  ["ADD_USER", "user2", "100"],
  ["MERGE_USER", "user1", "user2"],
]
```

Output:

```json
["true", "false", "50", "", "20", "", "true", "70"]
```

## 📕 Level 4 – Backup and Restore

Allows users to back up and restore their file state.

**BACKUP_USER <userId>**  
Saves the current state (file names and sizes) of all files owned by the user.  
Overwrites any previous backup.  
Returns the number of backed-up files, or empty string if user doesn't exist.

**RESTORE_USER <userId>**  
Restores the most recent backup for the user.  
Files owned by another user are skipped.  
Deletes current files if no backup exists.  
Returns the number of restored files, or an empty string if the user doesn’t exist.

**Notes:**
- `RESTORE_USER` does not delete the backup or affect user capacity.
- Deleted files are not backed up.

### 🔍 Example

```python
queries = [
  ["ADD_USER", "userA", "100"],
  ["ADD_FILE", "userA", "/file1", "20"],
  ["ADD_FILE", "userA", "/file2", "30"],
  ["BACKUP_USER", "userA"],
  ["DELETE_FILE", "/file1"],
  ["DELETE_FILE", "/file2"],
  ["RESTORE_USER", "userA"],
  ["GET_FILE_SIZE", "/file1"],
  ["GET_FILE_SIZE", "/file2"],
  ["ADD_USER", "userB", "10"],
  ["ADD_FILE", "userB", "/file1", "5"],
  ["RESTORE_USER", "userA"],
  ["GET_FILE_SIZE", "/file1"],
  ["GET_FILE_SIZE", "/file2"],
]
```

Output:

```json
["true", "80", "50", "2", "20", "30", "2", "20", "30", "true", "5", "1", "", "30"]
```
