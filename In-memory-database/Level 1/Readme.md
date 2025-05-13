# 📦 Class Structure Overview

## ✅ Record (Single Responsibility)
Encapsulates field-value pairs within a record.

**Methods:**
- `set_field()`
- `get_field()`
- `delete_field()`

## ✅ InMemoryRepository
Manages a dictionary of `key → Record`.

- Responsible for retrieving or creating records.
- Promotes **Open/Closed Principle** — can later be extended or replaced (e.g., with persistent storage) without modifying existing code.

## ✅ InMemoryDatabaseService
Coordinates command logic such as:
- `SET`
- `GET`
- `DELETE`

- Depends on `InMemoryRepository`, not its concrete implementation.
- Follows the **Dependency Inversion Principle** — high-level modules do not depend on low-level modules, but both depend on abstractions.
