
# 🔁 Banking System - Level 4

This level introduces the ability to **merge accounts** while preserving all balances, histories, and transaction integrity.

---

## ✅ What Was Added in Level 4

### 🔁 `merge_accounts(timestamp, acc1, acc2) -> bool`

Combines `acc2` into `acc1` with the following behavior:

- Transfers the **entire balance** from `acc2` to `acc1`
- Adds `acc2`'s **outgoing totals** into `acc1`
- Moves all **payment statuses** to `acc1`
- Merges **balance history** into `acc1` (as a snapshot at the time of merge)
- Tracks merges using `_mergeMap`

🗑️ Deletes all traces of `acc2` from:
- `_accounts`
- `_outgoingTotals`
- `_paymentStatus`
- `_accountHistory`

---

## 🧭 `_mergeMap` and `resolve_account(accountId)`

- Ensures all merged account references redirect to the **root surviving account**
- Applied in **all operations**: `deposit`, `pay`, `transfer`, etc.

---

## 🕒 `get_balance(timestamp, account_id, time_at) -> int | None`

- Returns the **balance at a specific timestamp** using historical snapshots
- Works even after merges by resolving to the current active account

---

## 🔁 `process_cashbacks(timestamp)`

- Handles **all due cashback refunds** scheduled for that timestamp
- Cashback originally scheduled for `acc2` is **redirected to `acc1`** if a merge occurred
- Cashback is processed **before any operation** at that timestamp

---

## 📈 History Tracking

- `_accountHistory` stores a list of `(timestamp, balance)` snapshots
- Updated after:
  - Every **deposit**
  - Every **withdrawal**
  - Every **cashback refund**

---

## 🧠 Summary

| Feature                  | Behavior |
|--------------------------|----------|
| ✅ Merge Accounts         | Combines balance, history, payments, and outgoing totals |
| ✅ Cashback Redirection   | Cashback of merged account refunded to the new account |
| ✅ History                | Tracks balance snapshots for `get_balance()` queries |
| ✅ Clean Mapping          | `_mergeMap` ensures transparent redirection of merged accounts |
| ✅ Safe Data Removal      | Fully deletes merged accounts from all system maps |

---
