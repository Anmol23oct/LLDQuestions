# file_repository.py

from file import File

class FileRepository:
    def __init__(self):
        self._storage = {}  # path -> (File, owner_user_id)

    def exists(self, path: str) -> bool:
        return path in self._storage

    def add(self, file: File, user_id: str) -> bool:
        if self.exists(file.path):
            return False
        self._storage[file.path] = (file, user_id)
        return True

    def get(self, path: str) -> File | None:
        entry = self._storage.get(path)
        return entry[0] if entry else None

    def get_owner(self, path: str) -> str | None:
        entry = self._storage.get(path)
        return entry[1] if entry else None

    def delete(self, path: str) -> tuple[File, str] | None:
        return self._storage.pop(path, None)

    def get_all(self) -> list[tuple[File, str]]:
        return list(self._storage.values())
