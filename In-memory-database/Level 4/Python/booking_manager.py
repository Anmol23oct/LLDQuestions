# backup_manager.py

class BackupManager:
    def __init__(self):
        self._snapshots = []  # list of (timestamp, snapshot)

    def save_snapshot(self, timestamp: int, current_data: dict[str, 'Record']) -> int:
        snapshot = {}
        for key, record in current_data.items():
            filtered = record.clone_with_remaining_ttl(timestamp)
            if filtered:
                snapshot[key] = filtered
        self._snapshots.append((timestamp, snapshot))
        return len(snapshot)

    def get_snapshot_before_or_at(self, timestamp_to_restore: int) -> tuple[int, dict[str, 'Record']] | None:
        result = None
        for ts, snap in self._snapshots:
            if ts <= timestamp_to_restore:
                result = (ts, snap)
            else:
                break
        return result
