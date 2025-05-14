# in_memory_repository.py

from record import Record

class InMemoryRepository:
    def __init__(self):
        self._records = {}  # key -> Record

    def get_or_create(self, key: str) -> Record:
        if key not in self._records:
            self._records[key] = Record()
        return self._records[key]

    def get_record(self, key: str) -> Record | None:
        return self._records.get(key)

    def get_all_records(self) -> dict[str, Record]:
        return self._records

    def set_all_records(self, records: dict[str, Record]):
        self._records = records
