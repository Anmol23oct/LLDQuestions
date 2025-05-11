# user.py

class User:
    def __init__(self, user_id: str, capacity: int):
        self.user_id = user_id
        self.capacity = capacity
        self.used = 0
        self.files = set()  # file paths owned by this user

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
