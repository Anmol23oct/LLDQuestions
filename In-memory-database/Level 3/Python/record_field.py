# record_field.py

class RecordField:
    def __init__(self, value: str, expires_at: int | None = None):
        self.value = value
        self.expires_at = expires_at

    def is_valid(self, timestamp: int) -> bool:
        return self.expires_at is None or timestamp < self.expires_at
