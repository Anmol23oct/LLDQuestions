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
