# record.py

from record_field import RecordField

class Record:
    def __init__(self):
        self.fields = {}  # field -> RecordField

    def set_field(self, field: str, value: str, timestamp: int | None = None, ttl: int | None = None):
        expires_at = timestamp + ttl if ttl is not None else None
        self.fields[field] = RecordField(value, expires_at)

    def get_field(self, field: str, timestamp: int | None = None) -> str:
        if field not in self.fields:
            return ""
        field_obj = self.fields[field]
        if timestamp is None or field_obj.is_valid(timestamp):
            return field_obj.value
        return ""

    def delete_field(self, field: str, timestamp: int | None = None) -> bool:
        if field not in self.fields:
            return False
        if timestamp is not None and not self.fields[field].is_valid(timestamp):
            return False
        del self.fields[field]
        return True

    def scan(self, timestamp: int | None = None) -> str:
        return self._format_fields(
            {f: rf for f, rf in self.fields.items()
             if timestamp is None or rf.is_valid(timestamp)}
        )

    def scan_by_prefix(self, prefix: str, timestamp: int | None = None) -> str:
        filtered = {
            f: rf for f, rf in self.fields.items()
            if f.startswith(prefix) and (timestamp is None or rf.is_valid(timestamp))
        }
        return self._format_fields(filtered)

    def _format_fields(self, fields: dict[str, RecordField]) -> str:
        return ", ".join(f"{field}({fields[field].value})" for field in sorted(fields))
