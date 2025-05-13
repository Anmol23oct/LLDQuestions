# record.py

class Record:
    def __init__(self):
        self.fields = {}  # field -> value

    def set_field(self, field: str, value: str):
        self.fields[field] = value

    def get_field(self, field: str) -> str:
        return self.fields.get(field, "")

    def delete_field(self, field: str) -> bool:
        if field in self.fields:
            del self.fields[field]
            return True
        return False

    def scan(self) -> str:
        return self._format_fields(self.fields)

    def scan_by_prefix(self, prefix: str) -> str:
        filtered = {
            field: val for field, val in self.fields.items() if field.startswith(prefix)
        }
        return self._format_fields(filtered)

    def _format_fields(self, fields: dict[str, str]) -> str:
        return ", ".join(f"{field}({fields[field]})" for field in sorted(fields))
