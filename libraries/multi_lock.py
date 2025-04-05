from typing import List
from .core_operations import CoreOperations
from .utilities.logger import VSNSLLogger

class MultiLockProcessor:
    """Handles multi-lock operations"""
    def __init__(self, core: CoreOperations):
        self.core = core
        self.logger = VSNSLLogger().logger

    def multi_encode(self, locks: List[int], data: str) -> str:
        """Sequential multi-lock encoding"""
        original_lock = self.core.encryption_lock
        result = data
        for lock in locks:
            self.core.encryption_lock = lock
            result = self.core.encode_data(result)
        self.core.encryption_lock = original_lock
        return result

    def multi_decode(self, locks: List[int], data: str) -> str:
        """Sequential multi-lock decoding"""
        original_lock = self.core.encryption_lock
        result = data
        for lock in reversed(locks):
            self.core.encryption_lock = lock
            result = self.core.decode_data(result)
        self.core.encryption_lock = original_lock
        return result 