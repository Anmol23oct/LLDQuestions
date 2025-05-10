
# 📘 Level 2 – Requirements Summary

## 🆕 `GET_LARGEST <prefix> <n>`

Return the top `n` files whose paths start with the given prefix.

### Sort by:
- Descending file size
- Lexicographically by path if sizes tie

### Format:
`"<path1>(<size1>), <path2>(<size2>), ..."`

If no matching files: return `""`.

---

## 🧱 Design Updates

We will update only the **FileService** layer.

### ✅ Why?

- **SRP**: `FileRepository` just stores/retrieves raw data.
- **FileService** knows how to:
  - Filter by prefix
  - Sort and format results
- **OCP**: Add new logic without modifying existing methods.
- **DIP**: Still depends on `FileRepository` interface.
