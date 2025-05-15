import heapq

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

        heap = []

        for worker in workers:
            # Create a max-heap using (-time, worker_id) to get proper order
            heapq.heappush(heap, (-worker.total_minutes, worker.worker_id, worker))

            if len(heap) > n:
                heapq.heappop(heap)

        # Now extract and sort the heap to build the result in proper descending order
        top_n = sorted(heap, key=lambda x: (-x[0], x[1]))  # sort by time desc, id asc

        return ", ".join(f"{worker.worker_id}({-score})" for score, _, worker in top_n)
