class Worker:
    def __init__(self, worker_id: str, position: str, compensation: int):
        self.worker_id = worker_id
        self.position = position
        self.compensation = compensation
        self.total_minutes = 0
        self.is_inside = False
        self.last_entry_time = None

    def register(self, timestamp: int) -> str:
        if not self.is_inside:
            self.is_inside = True
            self.last_entry_time = timestamp
        else:
            self.is_inside = False
            self.total_minutes += timestamp - self.last_entry_time
            self.last_entry_time = None
        return "registered"

    def get_total_minutes(self) -> str:
        return str(self.total_minutes)
