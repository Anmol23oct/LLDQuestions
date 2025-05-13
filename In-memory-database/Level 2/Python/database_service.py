# database_service.py

from in_memory_repository import InMemoryRepository

class InMemoryDatabaseService:
    def __init__(self, repository: InMemoryRepository):
        self.repo = repository

    def set(self, key: str, field: str, value: str) -> str:
        record = self.repo.get_or_create(key)
        record.set_field(field, value)
        return ""

    def get(self, key: str, field: str) -> str:
        record = self.repo.get_record(key)
        if not record:
            return ""
        return record.get_field(field)

    def delete(self, key: str, field: str) -> str:
        record = self.repo.get_record(key)
        if not record:
            return "false"
        return "true" if record.delete_field(field) else "false"

    def scan(self, key: str) -> str:
        record = self.repo.get_record(key)
        return record.scan() if record else ""

    def scan_by_prefix(self, key: str, prefix: str) -> str:
        record = self.repo.get_record(key)
        return record.scan_by_prefix(prefix) if record else ""
