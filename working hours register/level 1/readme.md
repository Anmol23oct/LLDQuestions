# 🕒 Contract Worker Time Tracking System – Level 1

## ✅ Objective

Your task is to implement a simplified version of a program registering the working hours of contract workers at a facility. All operations that should be supported by this program are described below.

Solving this task consists of several levels. Subsequent levels are opened when the current level is correctly solved. You always have access to the data for the current and all previous levels.

---

## 📋 Requirements

Plan your design according to the following level specification:

- **Level 1**: The working hours register program should support:
  - Adding workers to the system
  - Registering the time when workers enter or leave the office
  - Retrieving information about the time spent in the office

> ✅ To move to the next level, you need to pass all the tests at this level.

---

## 📦 Supported Operations

| Operation | Description |
|----------|-------------|
| `ADD_WORKER <workerId> <position> <compensation>` | Adds the `workerId` to the system and stores their position and compensation.<br>If the `workerId` already exists, returns `"false"`.<br>If successfully added, returns `"true"`.<br>Note: `workerId` and `position` contain only English letters and spaces. |
| `REGISTER <workerId> <timestamp>` | Registers either entry or exit time:<br>• If worker doesn't exist → `"invalid_request"`<br>• If not in office → registers **entry**<br>• If in office → registers **exit**<br>Returns `"registered"` if successful.<br>Note: timestamps strictly increase. |
| `GET <workerId>` | Returns total time worked using only **completed sessions** (entry and corresponding exit).<br>If worker hasn’t exited yet, the ongoing session is ignored.<br>If worker does not exist → returns `""` |

---

## 🧪 Example Execution

### 📥 Input Queries

```json
[
  "ADD_WORKER A Developer 100000",
  "ADD_WORKER A Manager 120000",
  "REGISTER A 10",
  "REGISTER A 25",
  "GET A",
  "REGISTER A 30",
  "REGISTER A 50",
  "REGISTER A 65",
  "GET A",
  "GET B",
  "REGISTER B 100"
]


[
  "true",
  "false",
  "registered",
  "registered",
  "15",
  "registered",
  "registered",
  "registered",
  "42",
  "",
  "invalid_request"
]
