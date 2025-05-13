# 🗃️ In-memory Database

## Requirements

Your task is to implement a simplified version of an in-memory database. Plan your design according to the level specifications below:

- **Level 1**: In-memory database should support basic operations to manipulate records, fields, and values within fields.
- **Level 2**: In-memory database should support displaying a specific record's fields based on a filter.
- **Level 3**: In-memory database should support TTL (Time-To-Live) configurations on database records.
- **Level 4**: In-memory database should support backup and restore functionality.

To move to the next level, you need to pass all the tests at this level.

> **Note**: You will receive a list of queries to the system, and the final output should be an array of strings representing the returned values of all queries. Each query will only call one operation.

---

## 🧩 Level 1

The basic level of the in-memory database contains records. Each record can be accessed with a unique identifier key of string type. A record may contain several field-value pairs, both of which are of string type.

- `SET <key> <field> <value>` — should insert a field-value pair to the record associated with key. If the field in the record already exists, replace the existing value with the specified value. If the record does not exist, create a new one. This operation should return an empty string.
- `GET <key> <field>` — should return the value contained within field of the record associated with key. If the record or the field doesn't exist, should return an empty string.
- `DELETE <key> <field>` — should remove the field from the record associated with key. Returns "true" if the field was successfully deleted, and "false" if the key or the field do not exist in the database.

### Examples

| Queries                         | Explanations                               |
|---------------------------------|--------------------------------------------|
| `["SET", "A", "B", "E"]`        | returns ""; database state: {"A": {"B": "E"}} |
| `["SET", "A", "C", "F"]`        | returns ""; database state: {"A": {"C": "F", "B": "E"}} |
| `["GET", "A", "B"]`             | returns "E"                                |
| `["GET", "A", "D"]`             | returns ""                                 |
| `["DELETE", "A", "B"]`          | returns "true"; database state: {"A": {"C": "F"}} |
| `["DELETE", "A", "D"]`          | returns "false"; database state: {"A": {"C": "F"}} |

---

## 🧩 Level 2

The database should support displaying data based on filters. Introduce an operation to support printing some fields of a record.

- `SCAN <key>` — should return a string representing the fields of a record associated with key. The returned string should be in the following format "`<field1>(<value1>), <field2>(<value2>), ...`", where fields are sorted lexicographically. If the specified record does not exist, returns an empty string.
- `SCAN_BY_PREFIX <key> <prefix>` — should return a string representing some fields of a record associated with key. Specifically, only fields that start with prefix should be included. The returned string should be in the same format as in the SCAN operation with fields sorted in lexicographical order.

### Examples

| Queries                                 | Explanations                                           |
|-----------------------------------------|--------------------------------------------------------|
| `["SET", "A", "BC", "E"]`               | returns ""; database state: {"A": {"BC": "E"}}         |
| `["SET", "A", "BD", "F"]`               | returns ""; database state: {"A": {"BC": "E", "BD": "F"}} |
| `["SET", "A", "C", "G"]`                | returns ""; database state: {"A": {"BC": "E", "BD": "F", "C": "G"}} |
| `["SCAN_BY_PREFIX", "A", "B"]`          | returns "BC(E), BD(F)"                                 |
| `["SCAN", "A"]`                         | returns "BC(E), BD(F), C(G)"                           |
| `["SCAN_BY_PREFIX", "B", "B"]`          | returns ""                                             |

The output should be `["", "", "", "BC(E), BD(F)", "BC(E), BD(F), C(G)", ""]`.

---

## 🧩 Level 3

Support the timeline of operations and TTL (Time-To-Live) settings for records and fields. Each operation from previous levels now has an alternative version with a timestamp parameter to represent when the operation was executed. For each field-value pair in the database, the TTL determines how long that value will persist before being removed.

> Notes:
> - Time should always flow forward, so timestamps are guaranteed to strictly increase as operations are executed.
> - Each test cannot contain both versions of operations (with and without timestamp). However, you should maintain backward compatibility.

### New Operations

- `SET_AT <key> <field> <value> <timestamp>`
- `SET_AT_WITH_TTL <key> <field> <value> <timestamp> <ttl>`
- `DELETE_AT <key> <field> <timestamp>`
- `GET_AT <key> <field> <timestamp>`
- `SCAN_AT <key> <timestamp>`
- `SCAN_BY_PREFIX_AT <key> <prefix> <timestamp>`

### Examples

#### Set 1

| Queries                                         | Explanations |
|------------------------------------------------|--------------|
| `["SET_AT_WITH_TTL", "A", "BC", "E", "1", "9"]` | returns ""; database state: {"A": {"BC": "E"}} with expiration at timestamp 10 |
| `["SET_AT_WITH_TTL", "A", "BC", "E", "5", "10"]` | returns ""; overwrite previous, expires at 15 |
| `["SET_AT", "A", "BD", "F", "5"]`              | returns ""; BD doesn't expire |
| `["SCAN_BY_PREFIX_AT", "A", "B", "14"]`         | returns "BC(E), BD(F)" |
| `["SCAN_BY_PREFIX_AT", "A", "B", "15"]`         | returns "BD(F)" |

Output: `["", "", "", "BC(E), BD(F)", "BD(F)"]`

#### Set 2

| Queries                                              | Explanations |
|------------------------------------------------------|--------------|
| `["SET_AT", "A", "B", "C", "1"]`                     | returns ""; state: {"A": {"B": "C"}} |
| `["SET_AT_WITH_TTL", "X", "Y", "Z", "2", "15"]`      | returns ""; expires at timestamp 17 |
| `["GET_AT", "X", "Y", "3"]`                          | returns "Z" |
| `["SET_AT_WITH_TTL", "A", "D", "E", "4", "10"]`      | expires at 14 |
| `["SCAN_AT", "A", "13"]`                             | returns "B(C), D(E)" |
| `["SCAN_AT", "X", "16"]`                             | returns "Y(Z)" |
| `["SCAN_AT", "X", "17"]`                             | returns "" |
| `["DELETE_AT", "X", "Y", "20"]`                      | returns "false" |

Output: `["", "", "Z", "", "B(C), D(E)", "Y(Z)", "", "false"]`

---

## 🧩 Level 4

The database should be backed up from time to time. Introduce operations to support backing up and restoring the database state based on timestamps. When restoring, ttl expiration times should be recalculated accordingly.

- `BACKUP <timestamp>` — saves the current state with remaining TTLs. Returns the number of non-empty, non-expired records.
- `RESTORE <timestamp> <timestampToRestore>` — restores the database to the latest backup before or at `timestampToRestore`. Recalculates expiration based on new time.

### Examples

| Queries                                                  | Explanations |
|----------------------------------------------------------|--------------|
| `["SET_AT_WITH_TTL", "A", "B", "C", "1", "10"]`          | returns ""; expires at 11 |
| `["BACKUP", "3"]`                                        | returns "1" |
| `["SET_AT", "A", "D", "E", "4"]`                         | returns "" |
| `["BACKUP", "5"]`                                        | returns "1" |
| `["DELETE_AT", "A", "B", "8"]`                           | returns "true" |
| `["BACKUP", "9"]`                                        | returns "1" |
| `["RESTORE", "10", "7"]`                                 | returns ""; "B" expires at 16 |
| `["BACKUP", "11"]`                                       | returns "1" |
| `["SCAN_AT", "A", "15"]`                                 | returns "B(C), D(E)" |
| `["SCAN_AT", "A", "16"]`                                 | returns "D(E)" |

Output: `["", "1", "", "1", "true", "1", "", "1", "B(C), D(E)", "D(E)"]`
