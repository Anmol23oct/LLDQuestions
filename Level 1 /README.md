
# 🧱 Class Design Overview

## 1. `Account` Class

**Attributes:**
- `accountId: String`
- `balance: double`

**Methods:**
- `deposit(amount: double): void`
- `withdraw(amount: double): boolean`
- `getBalance(): double`

---

## 2. `Transaction` Class

**Attributes:**
- `timestamp: long`
- `amount: double`
- `type: TransactionType` (e.g., `DEPOSIT`, `WITHDRAWAL`, `TRANSFER`)
- `sourceAccountId: String`
- `targetAccountId: String` *(nullable for deposits/withdrawals)*

**Methods:**
- `execute(): boolean`

---

## 3. `BankingSystem` Class

**Attributes:**
- `accounts: Map<String, Account>`
- `transactions: List<Transaction>`

**Methods:**
- `createAccount(accountId: String): boolean`
- `deposit(accountId: String, amount: double): boolean`
- `transfer(sourceAccountId: String, targetAccountId: String, amount: double): boolean`

---

# 📊 UML Class Diagram (Textual)

```
+----------------+
|   Account      |
+----------------+
| - accountId    |
| - balance      |
+----------------+
| + deposit()    |
| + withdraw()   |
| + getBalance() |
+----------------+

+----------------+
|  Transaction   |
+----------------+
| - timestamp    |
| - amount       |
| - type         |
| - sourceId     |
| - targetId     |
+----------------+
| + execute()    |
+----------------+

+----------------+
| BankingSystem  |
+----------------+
| - accounts     |
| - transactions |
+----------------+
| + createAccount() |
| + deposit()       |
| + transfer()      |
+----------------+
```

---

# 🧩 Applying SOLID Principles

### ✅ Single Responsibility Principle (SRP)
- `Account`: Manages account-specific operations.
- `Transaction`: Encapsulates logic for executing a transaction.
- `BankingSystem`: Coordinates accounts and transactions.

### ✅ Open/Closed Principle (OCP)
- You can introduce new types of `Transaction` without altering existing class logic.

### ✅ Liskov Substitution Principle (LSP)
- Derived `Transaction` classes can be used anywhere `Transaction` is expected.

### ✅ Interface Segregation Principle (ISP)
- Interface segregation is respected if we extract interfaces for specific operations.

### ✅ Dependency Inversion Principle (DIP)
- `BankingSystem` depends on `Transaction` abstraction, not on concrete implementations.

---

# 🛠️ Design Patterns Utilized

### 🏭 Factory Pattern
- Used to generate different `Transaction` objects (e.g., `DepositTransaction`, `TransferTransaction`).

### 🧠 Strategy Pattern
- Encapsulates different transaction execution logic and allows them to be interchanged dynamically.

---

---

# 🧱 Class Structure

1. **Account**: Manages balance and handles deposit/withdraw operations.
2. **Transaction** *(abstract base class)*: Represents all types of operations (e.g., deposit, withdrawal, transfer).
3. **BankingSystem**: Orchestrates account creation, transaction execution, and system-level queries.

---
