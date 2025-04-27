import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import inspect

class Logger:
    _instance = None
    
    def __new__(cls, name='VSNSL', log_level=logging.INFO, 
                log_file='resources/logs/activity.log', 
                max_bytes=5*1024*1024, backup_count=5):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, name='VSNSL', log_level=logging.INFO,
                 log_file=r'libraries\resources\logs\activity.log',
                 max_bytes=5*1024*1024, backup_count=5):
        if self._initialized:
            self.logger.info("[logger] Logger instance already initialized.")
            return
            
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Create logs directory if it doesn't exist
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"[logger] Log directory created or already exists: {log_path}")

        # Initialize default formatters with filename
        self.file_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        self.console_formatter = logging.Formatter('[%(levelname)s]: %(message)s')
        
        # File handler with rotation
        self.file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, 
            backupCount=backup_count, encoding='utf-8'
        )
        self.file_handler.setFormatter(self.file_formatter)
        self.logger.debug(f"[logger] File handler initialized with log file: {log_file}")

        # Console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.console_formatter)
        self.logger.debug("[logger] Console handler initialized.")

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        self.logger.info("[logger] Logger handlers added successfully.")
        self._initialized = True
        self.logger.info("[logger] Logger initialized successfully.")

    def set_file_formatter(self, fmt: str) -> bool:
        """Set custom format for file logs and signal success"""
        try:
            self.file_formatter = logging.Formatter(fmt)
            self.file_handler.setFormatter(self.file_formatter)
            self.logger.info("[logger] File formatter set successfully.")
            return True
        except Exception as e:
            self.logger.error(f"[logger] Failed to set file formatter: {e}")
            return False

    def set_console_formatter(self, fmt: str):
        """Set custom format for console logs"""
        try:
            self.console_formatter = logging.Formatter(fmt)
            self.console_handler.setFormatter(self.console_formatter)
            self.logger.info("[logger] Console formatter set successfully.")
            return True
        except Exception as e:
            self.logger.error(f"[logger] Failed to set console formatter: {e}")
            return False

    def _get_caller_file(self):
        """Get the name of the file that called the logger"""
        frame = inspect.stack()[2]
        return Path(frame.filename).stem

    def debug(self, message):
        self.logger.debug(f"[{self._get_caller_file()}] {message}")
        
    def info(self, message):
        self.logger.info(f"[{self._get_caller_file()}] {message}")
        
    def warning(self, message):
        self.logger.warning(f"[{self._get_caller_file()}] {message}")
        
    def error(self, message):
        self.logger.error(f"[{self._get_caller_file()}] {message}")
        
    def critical(self, message):
        self.logger.critical(f"[{self._get_caller_file()}] {message}")
        
    def log(self, level, message):
        self.logger.log(level, f"[{self._get_caller_file()}] {message}")

# Create a default instance for easy import
vsnsl_logger = Logger()
