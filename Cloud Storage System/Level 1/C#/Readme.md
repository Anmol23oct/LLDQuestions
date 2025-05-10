## 📦 Files & Responsibilities

### ✅ File.cs
- Represents a file using Path and Size.
- Follows SRP (just a data object).

### ✅ FileRepository.cs
- Manages internal file storage with Add, Get, and Delete.
- Uses Repository Pattern.
- Adheres to OCP and DIP principles.

### ✅ FileService.cs
- Coordinates the logic of adding, retrieving, and deleting files.
- Uses DIP by depending on FileRepository.
- Implements business logic (string responses) as expected.
