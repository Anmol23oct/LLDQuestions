# database_service.py

from in_memory_repository import InMemoryRepository

class InMemoryDatabaseService:
    def __init__(self, repository: InMemoryRepository):
        self.repo = repository

    def set(self, key: str, field: str, value: str) -> str:
        return self.set_at(key, field, value, timestamp=None)

    def set_at(self, key: str, field: str, value: str, timestamp: int | None) -> str:
        record = self.repo.get_or_create(key)
        record.set_field(field, value, timestamp)
        return ""

    def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int) -> str:
        record = self.repo.get_or_create(key)
        record.set_field(field, value, timestamp, ttl)
        return ""

    def get(self, key: str, field: str) -> str:
        return self.get_at(key, field, timestamp=None)

    def get_at(self, key: str, field: str, timestamp: int | None) -> str:
        record = self.repo.get_record(key)
        if not record:
            return ""
        return record.get_field(field, timestamp)

    def delete(self, key: str, field: str) -> str:
        return self.delete_at(key, field, timestamp=None)

    def delete_at(self, key: str, field: str, timestamp: int | None) -> str:
        record = self.repo.get_record(key)
        if not record:
            return "false"
        return "true" if record.delete_field(field, timestamp) else "false"

    def scan(self, key: str) -> str:
        return self.scan_at(key, timestamp=None)

    def scan_at(self, key: str, timestamp: int | None) -> str:
        record = self.repo.get_record(key)
        return record.scan(timestamp) if record else ""

    def scan_by_prefix(self, key: str, prefix: str) -> str:
        return self.scan_by_prefix_at(key, prefix, timestamp=None)

    def scan_by_prefix_at(self, key: str, prefix: str, timestamp: int | None) -> str:
        record = self.repo.get_record(key)
        return record.scan_by_prefix(prefix, timestamp) if record else ""
