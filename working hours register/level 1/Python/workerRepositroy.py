class WorkerRepository:
    def __init__(self):
        self._workers = {}  # worker_id -> Worker

    def add_worker(self, worker_id: str, position: str, compensation: int) -> str:
        if worker_id in self._workers:
            return "false"
        self._workers[worker_id] = Worker(worker_id, position, compensation)
        return "true"

    def get_worker(self, worker_id: str) -> Worker | None:
        return self._workers.get(worker_id)
