
# 💳 Banking System - Level 3

This level extends the banking system with support for **scheduled payments with cashback** and **payment status tracking**, in addition to existing features like account management, deposits, transfers, and top spender ranking.

---

## ✅ Features Implemented

### 1. `pay(timestamp, account_id, amount)`
- Withdraws the specified amount from the account.
- Provides **2% cashback** (rounded down) after **24 hours** (86,400,000 milliseconds).
- Returns a **unique paymentID** (e.g., `payment1`, `payment2`, ...).
- Updates the `top_spenders()` calculation — **pay withdrawals count as outgoing**.

---

### 2. `get_payment_status(timestamp, account_id, paymentID)`
- Returns payment status: `"IN_PROGRESS"` or `"CASHBACK_RECEIVED"`.
- Returns `None` for unknown accounts or mismatched payment IDs.

---

### 3. Cashback Processing
- Cashback is **processed before** any other transaction at that timestamp.
- Implemented using a **priority queue** (min-heap) based on cashback timestamp.

---

## 🧱 Design Highlights

### 🔍 SOLID Principles

| Principle | Application |
|-----------|-------------|
| **SRP** | Cashback logic is separated into its own processing step. |
| **OCP** | New transaction types like `PayTransaction` can be added without modifying existing code. |
| **LSP** | All transaction subclasses conform to a base type interface and behave consistently. |
| **ISP** | Interfaces not required yet, but planned for when external services are introduced. |
| **DIP** | `BankingSystem` depends only on abstractions (`Transaction`), not specific implementations. |

---

### 🧠 Design Patterns Used

- **Strategy Pattern**: Via polymorphic `Transaction.execute()` methods.
- **Priority Queue**: For scheduling and processing cashback efficiently.
- **Factory Pattern Ready**: Clean instantiation of transaction types through a centralized factory.

---

## 📦 File Overview

| Component | Description |
|-----------|-------------|
| **BankingSystem** | Core orchestration layer for all operations |
| **Account** | Manages balance, deposits, and withdrawals |
| **DepositTransaction**, **TransferTransaction** | Extend the `Transaction` base class |
| `pay()` / `get_payment_status()` | Directly handled by `BankingSystem` logic |
