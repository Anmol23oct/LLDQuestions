# file_service.py

from file import File
from file_repository import FileRepository
from user_repository import UserRepository

class FileService:
    def __init__(self, file_repo: FileRepository, user_repo: UserRepository):
        self.file_repo = file_repo
        self.user_repo = user_repo

    def add_user(self, user_id: str, capacity: int) -> str:
        return "true" if self.user_repo.add_user(user_id, capacity) else "false"

    def add_file(self, user_id: str, path: str, size: int) -> str:
        user = self.user_repo.get_user(user_id)
        if not user:
            return ""

        if self.file_repo.exists(path):
            old_file = self.file_repo.get(path)
            if self.file_repo.get_owner(path) != user_id:
                return ""
            user.delete_file(path, old_file.size)

        if not user.has_capacity(size):
            return ""

        new_file = File(path, size)
        self.file_repo.add(new_file, user_id)
        user.add_file(path, size)
        return str(user.get_remaining_capacity())

    def delete_file(self, path: str) -> str:
        entry = self.file_repo.delete(path)
        if not entry:
            return ""
        file, owner_id = entry
        owner = self.user_repo.get_user(owner_id)
        if owner:
            owner.delete_file(path, file.size)
        return str(file.size)

    def get_file_size(self, path: str) -> str:
        file = self.file_repo.get(path)
        return str(file.size) if file else ""

    def get_largest(self, prefix: str, n: int) -> str:
        all_files = [file for (file, _) in self.file_repo.get_all() if file.path.startswith(prefix)]
        if not all_files:
            return ""
        sorted_files = sorted(all_files, key=lambda f: (-f.size, f.path))
        top_files = sorted_files[:n]
        return ", ".join(f"{f.path}({f.size})" for f in top_files)

    def merge_user(self, user1_id: str, user2_id: str) -> str:
        result = self.user_repo.merge_users(user1_id, user2_id)
        return str(result) if result is not None else ""
