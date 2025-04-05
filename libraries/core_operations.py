from .utilities.logger import VSNSLLogger
from .charset import Charset

class CoreOperations:
    """Handles core encoding/decoding operations"""
    def __init__(self, charset: Charset, encryption_lock: int):
        self.logger = VSNSLLogger().logger
        self.charset = charset
        self.encryption_lock = encryption_lock if encryption_lock != 0 else 1

    def encode_data(self, data: str) -> str:
        """Original encoding logic"""
        encoded = []
        for char in data:
            if char in self.charset.charset:
                value = self.charset.charset[char] * self.encryption_lock
                encoded.append(str(value))
            else:
                self.logger.warning(f"Character {char} not found in charset")
                raise ValueError(f"Invalid character: {char}")
        return ''.join(encoded)

    def decode_data(self, data: str) -> str:
        """Original decoding logic"""
        decoded = []
        pairs = [data[i:i+3] for i in range(0, len(data), 3)]
        for pair in pairs:
            try:
                value = int(pair) // self.encryption_lock
                char = next(k for k, v in self.charset.charset.items() if v == value)
                decoded.append(char)
            except (ValueError, StopIteration):
                self.logger.error(f"Invalid pair: {pair}")
                raise ValueError("Decryption failed")
        return ''.join(decoded)

    def _get_key(self, value: int) -> str:
        """Original VSNSL.get_key implementation"""
        return next((k for k, v in self.charset.charset.items() if v == value), None) 