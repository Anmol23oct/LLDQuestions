# file_service.py

from file import File
from file_repository import FileRepository

class FileService:
    def __init__(self, repository: FileRepository):
        self.repo = repository

    def add_file(self, path: str, size: int) -> str:
        file = File(path, size)
        return "true" if self.repo.add(file) else "false"

    def get_file_size(self, path: str) -> str:
        file = self.repo.get(path)
        return str(file.size) if file else ""

    def delete_file(self, path: str) -> str:
        file = self.repo.delete(path)
        return str(file.size) if file else ""

    def get_largest(self, prefix: str, n: int) -> str:
        all_files = [file for file in self.repo._storage.values() if file.path.startswith(prefix)]
        if not all_files:
            return ""

        sorted_files = sorted(all_files, key=lambda f: (-f.size, f.path))
        top_files = sorted_files[:n]
        return ", ".join(f"{f.path}({f.size})" for f in top_files)
