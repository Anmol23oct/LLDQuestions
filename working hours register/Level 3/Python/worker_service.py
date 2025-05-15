# worker_service.py

class WorkerService:
    def __init__(self, repo: WorkerRepository):
        self.repo = repo

    def add_worker(self, worker_id: str, position: str, compensation: int) -> str:
        return self.repo.add_worker(worker_id, position, compensation)

    def register(self, worker_id: str, timestamp: int) -> str:
        worker = self.repo.get_worker(worker_id)
        return worker.register(timestamp) if worker else "invalid_request"

    def get_time(self, worker_id: str) -> str:
        worker = self.repo.get_worker(worker_id)
        return worker.get_total_minutes() if worker else ""

    def top_n_workers(self, n: int, position: str) -> str:
        workers = self.repo.get_workers_by_position(position)
        if not workers:
            return ""

        top_n = sorted(workers, key=lambda w: (-w.total_minutes, w.worker_id))[:n]
        return ", ".join(f"{w.worker_id}({w.total_minutes})" for w in top_n)

    def promote(self, worker_id: str, position: str, compensation: int, start_ts: int) -> str:
        worker = self.repo.get_worker(worker_id)
        return worker.promote(position, compensation, start_ts) if worker else "invalid_request"

    def calc_salary(self, worker_id: str, start: int, end: int) -> str:
        worker = self.repo.get_worker(worker_id)
        return worker.calc_salary(start, end) if worker else ""
