# file_repository.py

from file import File

class FileRepository:
    def __init__(self):
        self._storage = {}  # path -> File

    def exists(self, path: str) -> bool:
        return path in self._storage

    def add(self, file: File) -> bool:
        if self.exists(file.path):
            return False
        self._storage[file.path] = file
        return True

    def get(self, path: str) -> File | None:
        return self._storage.get(path)

    def delete(self, path: str) -> File | None:
        return self._storage.pop(path, None)
