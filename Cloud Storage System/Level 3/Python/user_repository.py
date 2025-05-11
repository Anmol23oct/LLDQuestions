# user_repository.py

from user import User

class UserRepository:
    def __init__(self):
        self.users = {}  # user_id -> User

    def add_user(self, user_id: str, capacity: int) -> bool:
        if user_id in self.users:
            return False
        self.users[user_id] = User(user_id, capacity)
        return True

    def get_user(self, user_id: str) -> User | None:
        return self.users.get(user_id)

    def delete_user(self, user_id: str):
        if user_id in self.users:
            del self.users[user_id]

    def merge_users(self, user1_id: str, user2_id: str) -> int | None:
        if user1_id == "admin" or user2_id == "admin":
            return None
        if user1_id not in self.users or user2_id not in self.users:
            return None

        user1 = self.users[user1_id]
        user2 = self.users[user2_id]

        for file_path in user2.files:
            user1.files.add(file_path)

        user1.used += user2.used
        user1.capacity += user2.capacity

        self.delete_user(user2_id)
        return user1.get_remaining_capacity()
