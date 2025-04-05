from .core_operations import CoreOperations
from .utilities.logger import VSNSLLogger

class BatchProcessor:
    """Handles batch encoding/decoding"""
    def __init__(self, core: CoreOperations):
        self.core = core
        self.logger = VSNSLLogger().logger

    def encode_batch(self, data_list: list) -> list:
        """Process batch encoding"""
        results = []
        for data in data_list:
            try:
                results.append(self.core.encode_data(data))
            except Exception as e:
                self.logger.error(f"Batch encode failed: {str(e)}")
                results.append(None)
        return results

    def decode_batch(self, encoded_list: list) -> list:
        """Process batch decoding"""
        results = []
        for data in encoded_list:
            try:
                results.append(self.core.decode_data(data))
            except Exception as e:
                self.logger.error(f"Batch decode failed: {str(e)}")
                results.append(None)
        return results 