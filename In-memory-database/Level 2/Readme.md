# 🗃️ In-Memory Database – Level 2

## ✅ Objective

Enhance the in-memory database to support filtered field retrieval for a given record.

---

## 📦 Features Implemented

1. **SET <key> <field> <value>**  
   Adds or updates a field-value pair for the given key.  
   Creates the record if the key doesn't exist.  
   **Returns**: `""`

2. **GET <key> <field>**  
   Retrieves the value of a specific field in the record.  
   **Returns**: Value string or `""` if not found.

3. **DELETE <key> <field>**  
   Removes the specified field from the record.  
   **Returns**: `"true"` if deleted, `"false"` otherwise.

4. **SCAN <key>**  
   Returns all field-value pairs for the given key in the format:  
   `"<field1>(<value1>), <field2>(<value2>), ..."`  
   Fields are sorted lexicographically.  
   **Returns**: Formatted string or `""` if the record doesn't exist.

5. **SCAN_BY_PREFIX <key> <prefix>**  
   Returns only fields starting with the given prefix.  
   Format is the same as SCAN, and fields are sorted.  
   **Returns**: Filtered formatted string or `""` if no match.

---

## 🧱 Architecture

### ✅ Record class  
Manages all field-value operations for a record.  

**Added**:  
- `scan()`: returns all fields sorted.  
- `scan_by_prefix(prefix)`: returns filtered fields sorted.

### ✅ InMemoryRepository  
Stores a mapping of `key -> Record`.

**Methods**:  
- `get_record()`, `get_or_create()`

### ✅ InMemoryDatabaseService  
Coordinates record operations and query responses.  

**New methods**:  
- `scan(key)`  
- `scan_by_prefix(key, prefix)`

---

## 🧪 Example Queries

| Query                             | Result               |
|----------------------------------|----------------------|
| `["SET", "A", "BC", "E"]`        | `""`                 |
| `["SET", "A", "BD", "F"]`        | `""`                 |
| `["SET", "A", "C", "G"]`         | `""`                 |
| `["SCAN_BY_PREFIX", "A", "B"]`   | `"BC(E), BD(F)"`     |
| `["SCAN", "A"]`                  | `"BC(E), BD(F), C(G)"` |
| `["SCAN_BY_PREFIX", "B", "B"]`   | `""`                 |
