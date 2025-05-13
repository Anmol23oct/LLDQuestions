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
