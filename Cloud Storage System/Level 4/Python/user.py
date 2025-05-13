# user.py

class User:
    def __init__(self, user_id: str, capacity: int):
        self.user_id = user_id
        self.capacity = capacity
        self.used = 0
        self.files = set()
        self._backup = None  # path -> size

    def has_capacity(self, size: int) -> bool:
        return (self.capacity - self.used) >= size

    def add_file(self, path: str, size: int):
        self.files.add(path)
        self.used += size

    def delete_file(self, path: str, size: int):
        if path in self.files:
            self.files.remove(path)
            self.used -= size

    def get_remaining_capacity(self) -> int:
        return self.capacity - self.used

    def backup(self, file_sizes: dict[str, int]) -> int:
        self._backup = {
            path: file_sizes[path] for path in self.files if path in file_sizes
        }
        return len(self._backup)

    def restore(self, get_owner: callable, restore_file: callable) -> int:
        if not self._backup:
            return 0

        for path in list(self.files):
            self.delete_file(path, 0)

        restored = 0
        for path, size in self._backup.items():
            owner = get_owner(path)
            if owner is None or owner == self.user_id:
                self.add_file(path, size)
                restore_file(path, size)
                restored += 1

        return restored
