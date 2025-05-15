# 👷‍♂️ Level 3 – Worker Promotion and Salary Calculation System

## 📝 Overview
In this level, we extend the worker attendance system with:

- **PROMOTE**: Support for tracking promotions and salary changes based on office re-entry.
- **CALC_SALARY**: Calculation of salary within a time window, factoring in different compensations for different roles.
- Enhancements to `TOP_N_WORKERS` and `GET` to account for role-based filtering and time aggregation.

---

## 🧾 Supported Commands

### ➕ `ADD_WORKER <workerId> <position> <compensation>`
Adds a new worker with an initial position and hourly compensation.  
**Returns:** `"registered"`

---

### ⏱ `REGISTER <workerId> <timestamp>`
Toggles worker’s entry/exit at the specified timestamp.  
- If entering: starts a new office session.  
- If exiting: ends the session.  
**Returns:** `"registered"`

---

### 🚀 `PROMOTE <workerId> <newPosition> <newCompensation> <startTimestamp>`
Schedules a promotion (with position and compensation) to take effect **only when the worker re-enters the office** after or at `startTimestamp`.

**Returns:**
- `"success"` if promotion is registered and not yet applied.
- `"invalid_request"` if the worker was already promoted or does not exist.

---

### 💰 `CALC_SALARY <workerId> <startTimestamp> <endTimestamp>`
Calculates salary over the given period considering:
- Only **completed** sessions.
- Compensation **during that session** (which may change due to promotions).

**Returns:** total salary as string (e.g. `"35000"`), or `""` if worker not found.

---

### 📈 `TOP_N_WORKERS <n> <position>`
Returns top `n` workers with the **current** position sorted by:
1. Total time spent (descending),
2. Alphabetically by worker ID (tie-breaker).  
**Returns:** e.g. `"John(75), Alice(60)"` or `""`.

---

### 📊 `GET <workerId>`
Returns total time spent **across all positions**, even old ones.  
**Returns:** total time as string (e.g. `"250"`)

---

## ✅ Example Input and Expected Output

```python
queries = [
  ["ADD_WORKER", "John", "Middle Developer", "200"],
  ["REGISTER", "John", "0"],
  ["REGISTER", "John", "25"],
  ["PROMOTE", "John", "Senior Developer", "500", "200"],
  ["REGISTER", "John", "100"],
  ["REGISTER", "John", "125"],
  ["PROMOTE", "John", "Senior Developer", "500", "200"],
  ["REGISTER", "John", "150"],
  ["REGISTER", "John", "300"],
  ["CALC_SALARY", "John", "0", "500"],
  ["TOP_N_WORKERS", "3", "Senior Developer"],
  ["REGISTER", "John", "350"],
  ["REGISTER", "John", "325"],
  ["GET", "John"],
  ["TOP_N_WORKERS", "10", "Middle Developer"],
  ["CALC_SALARY", "John", "110", "350"],
  ["CALC_SALARY", "John", "900", "1400"]
]
📤 Expected Output
python
Copy
Edit
[
  "true",              # Add worker
  "registered",        # Enter at 0
  "registered",        # Exit at 25
  "success",           # Promotion scheduled
  "registered",        # Enter at 100
  "invalid_request",   # Promotion repeat
  "registered",        # Exit at 125
  "registered",        # Enter at 150
  "registered",        # Exit at 300
  "35000",             # Salary = 25*200 + 25*200 + 75*200 = 35000
  "John(0)",           # Still hasn't re-entered post promotion
  "registered",        # Enter at 350 (promotion kicks in)
  "registered",        # Exit at 325 (session invalid - backward)
  "250",               # Total time = 25+25+150 = 250
  "John(75)",          # Time in Middle Dev only
  "",                  # Worker not found or invalid session
  "45500",             # Salary = 15*200 + 150*200 + 25*500 = 45500
  "0"                  # No session in the time range
]
📌 Notes
PROMOTE doesn't take effect immediately, only after a re-entry past startTimestamp.

Salary is computed only for completed sessions.

GET aggregates across all roles, while TOP_N_WORKERS only considers the current role.
