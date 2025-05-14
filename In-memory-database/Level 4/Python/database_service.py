# database_service.py

from in_memory_repository import InMemoryRepository
from backup_manager import BackupManager

class InMemoryDatabaseService:
    def __init__(self, repository: InMemoryRepository):
        self.repo = repository
        self.backup_mgr = BackupManager()

    def set(self, key: str, field: str, value: str) -> str:
        return self.set_at(key, field, value, None)

    def set_at(self, key: str, field: str, value: str, timestamp: int | None) -> str:
        record = self.repo.get_or_create(key)
        record.set_field(field, value, timestamp)
        return ""

    def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int) -> str:
        record = self.repo.get_or_create(key)
        record.set_field(field, value, timestamp, ttl)
        return ""

    def get(self, key: str, field: str) -> str:
        return self.get_at(key, field, None)

    def get_at(self, key: str, field: str, timestamp: int | None) -> str:
        record = self.repo.get_record(key)
        return record.get_field(field, timestamp) if record else ""

    def delete(self, key: str, field: str) -> str:
        return self.delete_at(key, field, None)

    def delete_at(self, key: str, field: str, timestamp: int | None) -> str:
        record = self.repo.get_record(key)
        return "true" if record and record.delete_field(field, timestamp) else "false"

    def scan(self, key: str) -> str:
        return self.scan_at(key, None)

    def scan_at(self, key: str, timestamp: int | None) -> str:
        record = self.repo.get_record(key)
        return record.scan(timestamp) if record else ""

    def scan_by_prefix(self, key: str, prefix: str) -> str:
        return self.scan_by_prefix_at(key, prefix, None)

    def scan_by_prefix_at(self, key: str, prefix: str, timestamp: int | None) -> str:
        record = self.repo.get_record(key)
        return record.scan_by_prefix(prefix, timestamp) if record else ""

    def backup(self, timestamp: int) -> str:
        current_data = self.repo.get_all_records()
        count = self.backup_mgr.save_snapshot(timestamp, current_data)
        return str(count)

    def restore(self, now: int, timestamp_to_restore: int) -> str:
        result = self.backup_mgr.get_snapshot_before_or_at(timestamp_to_restore)
        if not result:
            return ""
        snapshot_time, snapshot = result
        restored = {}
        for key, record in snapshot.items():
            updated = record.clone_with_remaining_ttl(snapshot_time)
            if updated:
                for field in updated.fields.values():
                    if field.expires_at is not None:
                        field.expires_at = now + (field.expires_at - snapshot_time)
                restored[key] = updated
        self.repo.set_all_records(restored)
        return ""
