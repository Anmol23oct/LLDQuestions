# 🧑‍💻 Level 2 – Contract Worker Time Tracking System

## ✅ Objective

Extend the existing worker time tracking system to support ordered statistics retrieval based on working hours and job position.

---

## 🆕 New Operation

### `TOP_N_WORKERS <n> <position>`

Returns the top **n** workers (by total time spent in the office) with a given **position**.

#### 📌 Format:
```plaintext
"workerId1(timeSpentInOffice1), workerId2(timeSpentInOffice2), ..., workerIdN(timeSpentInOfficeN)"
📚 Rules:
Count only finished work sessions (i.e., complete entry and exit pairs).

If a worker has no finished session, their time is 0.

Workers are sorted:

By time spent in descending order.

Alphabetically by workerId in case of tie.

If fewer than n workers exist for the position, return all matching workers.

If no workers exist with the given position, return an empty string.

🧾 Input Format
An array of queries. Each query can be one of the following:

python
Copy
Edit
["ADD_WORKER", workerId, position, salary]
["REGISTER", workerId, timestamp]
["TOP_N_WORKERS", n, position]
📤 Output
An array of strings, each corresponding to the result of the executed query.

🧪 Example Test Case
🔢 Input
python
Copy
Edit
queries = [
  ["ADD_WORKER", "John",  "Junior Developer", "120"],
  ["ADD_WORKER", "Jason", "Junior Developer", "120"],
  ["ADD_WORKER", "Ashley","Junior Developer", "120"],
  ["REGISTER", "John", "100"],
  ["REGISTER", "John", "150"],
  ["REGISTER", "Jason", "200"],
  ["REGISTER", "Jason", "250"],
  ["REGISTER", "Jason", "275"],
  ["TOP_N_WORKERS", "5", "Junior Developer"],
  ["TOP_N_WORKERS", "1", "Junior Developer"],
  ["REGISTER", "Ashley", "400"],
  ["REGISTER", "Ashley", "500"],
  ["REGISTER", "Jason", "575"],
  ["TOP_N_WORKERS", "3", "Junior Developer"],
  ["TOP_N_WORKERS", "3", "Middle Developer"]
]
✅ Output
python
Copy
Edit
[
  "true",
  "true",
  "true",
  "registered",
  "registered",
  "registered",
  "registered",
  "registered",
  "Jason(50), John(50), Ashley(0)",
  "Jason(50)",
  "registered",
  "registered",
  "registered",
  "Jason(350), Ashley(100), John(50)",
  ""
]
