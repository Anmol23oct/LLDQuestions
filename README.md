
# 🏦 Simplified Banking System Challenge

## 📜 Instructions

Your task is to implement a simplified version of a banking system. The problem is divided into multiple levels. You unlock the next level only after correctly implementing the current one.

You always have access to the data and functionality of all previous levels.

⏳ Execute a single test case with:
```bash
bash run_single_test.sh "<test_case_name>"
```

---

## ✅ Requirements

Each function will include a `timestamp: int` parameter (in milliseconds). All timestamps are:
- Unique
- In strictly increasing order
- Within the range [1, 10^9]

---

## 🧩 Levels Overview

### 🟢 Level 1: Account Creation, Deposits & Transfers

#### API Methods

- `create_account(timestamp: int, account_id: str) -> bool`
  - Returns `True` if account is created, `False` if it already exists.

- `deposit(timestamp: int, account_id: str, amount: int) -> int | None`
  - Returns new balance or `None` if account doesn't exist.

- `transfer(timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None`
  - Returns new balance of source account or `None` if:
    - Either account doesn't exist
    - Same source & target account
    - Insufficient funds

#### 🧪 Example Queries

| Query | Result | Reason |
|--|--|--|
| `create_account(1, "account1")` | `True` | Account created |
| `create_account(2, "account1")` | `False` | Already exists |
| `deposit(5, "account1", 2700)` | `2700` | Successful deposit |
| `transfer(6, "account1", "account2", 2701)` | `None` | Insufficient funds |

---

### 🟡 Level 2: Ranking Top Spenders

#### API Method

- `top_spenders(timestamp: int, n: int) -> list[str]`
  - Return top `n` accounts by **total outgoing** amount (withdrawals + transfers).
  - Format: `["account_id(amount)", ...]`
  - Sort by amount (desc) → account ID (asc)

#### 🧪 Example Queries

| Query | Result |
|--|--|
| `top_spenders(7, 3)` | `['account1(0)', 'account2(0)', 'account3(0)']` |
| `transfer(8, "account3", "account2", 500)` | ... |
| `top_spenders(11, 3)` | `['account1(2500)', 'account3(1500)', 'account2(0)']` |

---

### 🟠 Level 3: Payments & Cashback

#### API Methods

- `pay(timestamp: int, account_id: str, amount: int) -> str | None`
  - Withdraws funds and returns a unique ID (e.g., `payment1`)
  - 2% cashback (rounded down) processed **after 24 hours**

- `get_payment_status(timestamp: int, account_id: str, payment: str) -> str | None`
  - Returns `"IN_PROGRESS"` or `"CASHBACK_RECEIVED"` if valid
  - Else `None`

> 💡 Cashback is credited at `timestamp + 86400000` ms.

#### 🧪 Example Queries

| Query | Result |
|--|--|
| `pay(4, "account1", 1000)` | `"payment1"` |
| `get_payment_status(103, "account1", "payment1")` | `"IN_PROGRESS"` |
| `get_payment_status(4 + 86400000, "account1", "payment1")` | `"CASHBACK_RECEIVED"` |

---

### 🔴 Level 4: Merging Accounts & Historical Balances

#### API Methods

- `merge_accounts(timestamp: int, account_id_1: str, account_id_2: str) -> bool`
  - Merges `account_id_2` into `account_id_1`
  - Refunds from pending payments are applied to `account_id_1`
  - `account_id_2` is removed

- `get_balance(timestamp: int, account_id: str, time_at: int) -> int | None`
  - Returns balance of an account at `time_at`
  - If account was merged, balance reflects new state

#### 🧪 Example Queries

| Query | Result | Description |
|--|--|--|
| `merge_accounts(9, "account1", "account2")` | `True` | Successful merge |
| `get_balance(10, "account1", 10)` | `3000` | Combined balance |
| `get_balance(11, "account2", 10)` | `None` | Account no longer exists |

---

## 📌 Constraints

- 🕒 **Execution Time Limit:** 3 seconds  
- 💾 **Memory Limit:** 1 GB

---

## 🔁 Notes

- Cashback processing occurs *before* any other operations at its timestamp.
- All operations must honor the order and uniqueness of timestamps.
- Merged accounts must preserve:
  - Transaction history
  - Refunds
  - Balance tracking

---
