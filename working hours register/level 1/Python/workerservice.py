class WorkerService:
    def __init__(self, repo: WorkerRepository):
        self.repo = repo

    def add_worker(self, worker_id: str, position: str, compensation: int) -> str:
        return self.repo.add_worker(worker_id, position, compensation)

    def register(self, worker_id: str, timestamp: int) -> str:
        worker = self.repo.get_worker(worker_id)
        if not worker:
            return "invalid_request"
        return worker.register(timestamp)

    def get_time(self, worker_id: str) -> str:
        worker = self.repo.get_worker(worker_id)
        return worker.get_total_minutes() if worker else ""
