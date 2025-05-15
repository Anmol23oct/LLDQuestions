# worker.py

class Worker:
    def __init__(self, worker_id: str, position: str, compensation: int):
        self.worker_id = worker_id
        self.position = position
        self.compensation = compensation

        self.total_minutes = 0
        self.is_inside = False
        self.last_entry_time = None

        self.sessions = []  # list of (start, end, position, compensation)

        self.pending_position = None
        self.pending_compensation = None
        self.promotion_start_timestamp = None

    def register(self, timestamp: int) -> str:
        if not self.is_inside:
            # Handle promotion if pending
            if (
                self.pending_position is not None
                and timestamp >= self.promotion_start_timestamp
            ):
                self.position = self.pending_position
                self.compensation = self.pending_compensation
                self.pending_position = None
                self.pending_compensation = None
                self.promotion_start_timestamp = None

            self.is_inside = True
            self.last_entry_time = timestamp
        else:
            # Exit
            self.is_inside = False
            if self.last_entry_time is not None:
                duration = timestamp - self.last_entry_time
                self.total_minutes += duration
                self.sessions.append(
                    (
                        self.last_entry_time,
                        timestamp,
                        self.position,
                        self.compensation,
                    )
                )
                self.last_entry_time = None
        return "registered"

    def get_total_minutes(self) -> str:
        return str(self.total_minutes)

    def promote(self, new_position: str, new_comp: int, start_time: int) -> str:
        if (
            self.pending_position is not None
            or self.position == new_position
            or self.is_inside
        ):
            return "invalid_request"

        self.pending_position = new_position
        self.pending_compensation = new_comp
        self.promotion_start_timestamp = start_time
        return "success"

    def calc_salary(self, start: int, end: int) -> str:
        if not self.sessions:
            return "0"

        total_salary = 0
        for s_start, s_end, pos, comp in self.sessions:
            # Only consider overlapping sessions
            overlap_start = max(start, s_start)
            overlap_end = min(end, s_end)
            if overlap_start < overlap_end:
                total_salary += (overlap_end - overlap_start) * comp

        return str(total_salary)
