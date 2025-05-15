# worker_repository.py

class WorkerRepository:
    def __init__(self):
        self._workers = {}

    def add_worker(self, worker_id: str, position: str, compensation: int) -> str:
        if worker_id in self._workers:
            return "false"
        self._workers[worker_id] = Worker(worker_id, position, compensation)
        return "true"

    def get_worker(self, worker_id: str):
        return self._workers.get(worker_id)

    def get_workers_by_position(self, position: str) -> list:
        return [w for w in self._workers.values() if w.position == position]
