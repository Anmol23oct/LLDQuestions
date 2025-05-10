🧱 Class Design Overview
1. Account
Attributes:

accountId: String

balance: double

Methods:

deposit(amount: double): void

withdraw(amount: double): boolean

getBalance(): double

2. Transaction
Attributes:

timestamp: long
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


amount: double

type: TransactionType (e.g., DEPOSIT, WITHDRAWAL, TRANSFER)

sourceAccountId: String

targetAccountId: String (nullable for deposits/withdrawals)

Methods:

execute(): boolean

3. BankingSystem
Attributes:

accounts: Map<String, Account>

transactions: List<Transaction>

Methods:

createAccount(accountId: String): boolean

deposit(accountId: String, amount: double): boolean

transfer(sourceAccountId: String, targetAccountId: String, amount: double): boolean

📊 UML Class Diagram
Here's a textual representation of the UML class diagram:

pgsql
Copy
Edit
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
🧩 Applying SOLID Principles
Single Responsibility Principle (SRP):

Each class has a single responsibility:

Account handles account-related operations.

Transaction handles transaction execution.

BankingSystem manages accounts and transactions.

Open/Closed Principle (OCP):

The system is open for extension but closed for modification.

New transaction types can be added by extending the Transaction class without modifying existing code.

Liskov Substitution Principle (LSP):

Subclasses of Transaction can be used interchangeably with the base class without altering the correctness of the program.

Interface Segregation Principle (ISP):

Interfaces (if introduced) should be specific to client needs to avoid forcing classes to implement unnecessary methods.

Dependency Inversion Principle (DIP):

High-level modules (BankingSystem) depend on abstractions (Transaction), not on concrete implementations.

🛠️ Design Patterns Utilized
Factory Pattern:

To create different types of transactions (DepositTransaction, TransferTransaction) based on input parameters.

Strategy Pattern:

To encapsulate algorithms for different transaction types, allowing them to be interchangeable.
